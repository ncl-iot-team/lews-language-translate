from procstream import StreamProcessMicroService
import os
from googletrans import Translator
import logging as logger

config = {"MODULE_NAME": os.environ.get('MODULE_NAME', 'LEWS_LANG_DETECT'),
          "CONSUMER_GROUP": os.environ.get("CONSUMER_GROUP", "LEWS_LANG_DETECT_CG")}


class StreamProcessLanguageTranslateService(StreamProcessMicroService):
    def __init__(self, config_new, translator_obj):
        super().__init__(config_new)
        self.translator_obj = translator_obj

    def process_message(self, message):
        payload = message.value
        try:
            original_text = payload.get('text')
            if payload.get('lews_meta_detected_lang') != 'en':
                translated_text = self.translator_obj.translate(original_text).text
                payload['lews_meta_original_text'] = original_text
                payload['text'] = translated_text
        except:
            logger.error(f"Cannot translate:{payload}")
        #print(payload)
        return payload


def main():
    translator_obj = Translator()
    k_service = StreamProcessLanguageTranslateService(config, translator_obj)
    k_service.start_service()


if __name__ == "__main__":
    main()
