import globalPluginHandler, ui, speech
from stackspot import Stackspot

""" Um exemplo de execução de integração com stackspot com entrada de estimulo NVDA"""


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    def script_runStackSpot(self, gesture):
        prompt = ui.getInput("Prompt para o agente StackSpot:")
        if not prompt:
            return
        client = Stackspot.instance()
        execution = client.ai.quick_command.create_execution('my-quick-command-slug', prompt)
        execution = client.ai.quick_command.poll_execution(execution)
        resp = execution.get('result', 'Sem resposta')
        speech.speakText(resp)

    __gestures = {
        "kb:NVDA+alt+S": "runStackSpot"
    }
