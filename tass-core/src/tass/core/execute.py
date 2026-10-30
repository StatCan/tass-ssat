import json
from pathlib import Path
from .parser.parse import parse
from .log.logging import getLogger, init_base_logger, closeLoggerFile
from .context import ctx
from tass.core.hooks.dispatcher import HookDispatcher
from tass.core.hooks.hook_cfg import HookEvent


log = None


class TassEncoder(json.JSONEncoder):
    # Convert Python objects to JSON equivalent.
    # TODO: Update format to match test management tool
    def default(self, obj):
        """
        Default JSON encoder
        for custom TASS classes.
        Serializable TASS classes should
        implement the toJson function.
        """
        if (isinstance(obj, object)):
            if (hasattr(obj, 'toJson')):
                return obj.toJson()
            elif isinstance(obj, Exception):
                return {"error": obj.__class__.__name__, "message": str(obj)}
        return super().default(obj)


def init_loggers(run_logging, test_logging, log_level):
    init_base_logger(run_logging=run_logging,
                     test_logging=test_logging,
                     log_level=log_level)
    return getLogger(__name__)

def execute(file_paths, no_validate, run_logging, test_logging, log_level):
    log = init_loggers(
                run_logging,
                test_logging,
                log_level)
    log.info("\n\n <<<<<< TASS Starting >>>>>> \n\n")
    for file_path in file_paths:
        try:
            path = Path(file_path).resolve()

            run = parse(path, no_validate)
            dispatcher = HookDispatcher()
            ctx.run_uuid.value = run.uuid
            ctx.run_name.value = run.title
            ctx.run_id.value = run.id

            log.info("<<<<< Starting Run: %s >>>>>", run.uuid)
            dispatcher.fire(HookEvent.BEFORE_RUN, run.hooks)
            
            for case in run.collect():
                try:
                    log.info("")
                    log.info("< < < Starting Case: %s > > >", case.uuid)
                    log.info("")

                    ctx.test_uuid.value = case.uuid
                    ctx.test_name.value = case.title
                    ctx.test_id.value = case.id
                    dispatcher.fire(HookEvent.BEFORE_TEST, run.hooks + case.hooks)
                    case.execute_tass(dispatcher.fire)

                    log.info("")
                    log.info("> > > Finished Case: %s < < <", case.uuid)
                    log.info("")
                finally:
                    dispatcher.fire(HookEvent.AFTER_TEST, run.hooks + case.hooks)
                    closeLoggerFile(ctx.test_id.value)
                    ctx.test_id.reset()
                    ctx.test_uuid.reset()
                    ctx.test_name.reset()

            Path('results').mkdir(exist_ok=True)

            file_name = run.uuid + '---' + run.start_time + '.json'
            result_path = Path().resolve() / "results" / file_name
            try:
                f = open(result_path, 'w+', encoding='utf-8')
            except IOError as e:
                log.error("An IOError occured: %s" % e)
                return
            with f:
                json.dump(run, f, indent=4, cls=TassEncoder)
        finally:
            dispatcher.fire(HookEvent.AFTER_RUN, run.hooks)
            closeLoggerFile(ctx.run_id.value)
            ctx.run_id.reset()
            ctx.run_name.reset()
            ctx.run_uuid.reset()

            dispatcher.unwind_all()


