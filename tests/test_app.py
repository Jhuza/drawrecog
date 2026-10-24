from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import sys
import numpy as np
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def test_blank_key_drawing_request_and_stale_result():
    canvas = SimpleNamespace(image_data=np.full((32,32,4),255,dtype=np.uint8), json_data={'objects':[]})
    result = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content='Una línea diagonal.'))])
    with patch('streamlit_drawable_canvas.st_canvas',return_value=canvas), patch('openai.OpenAI') as client:
        client.return_value.__enter__.return_value.chat.completions.create.return_value=result
        app = AppTest.from_file(str(ROOT/'app.py')).run(timeout=30)
        app.button[0].click().run()
        assert app.warning and not client.called
        app.text_input[0].input('test-not-a-real-key').run()
        app.button[0].click().run()
        assert app.warning and not client.called
        canvas.json_data['objects']=[{'type':'path'}]
        canvas.image_data[8:24,16,:3]=0
        app.run()
        app.button[0].click().run()
        assert not app.exception
        request=client.return_value.__enter__.return_value.chat.completions.create.call_args.kwargs
        assert request['model']=='gpt-4o-mini' and request['max_tokens']==500
        assert request['messages'][0]['content'][1]['image_url']['url'].startswith('data:image/png;base64,')
        assert app.session_state['sketch_response']=='Una línea diagonal.'
        app.run()
        assert app.session_state['sketch_response']=='Una línea diagonal.'
        canvas.image_data[4,4,:3]=0
        app.run()
        assert 'sketch_response' not in app.session_state
