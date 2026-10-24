import base64
import hashlib
import io
import numpy as np
import streamlit as st
from PIL import Image
from openai import OpenAI
from streamlit_drawable_canvas import st_canvas
from aurora import app_header, footer, section

app_header()
with st.sidebar:
    stroke=st.slider("Grosor del trazo",1,30,5)
    st.caption("Dibuja en negro sobre blanco. La descripción se genera al pulsar Interpretar boceto.")
left,right=st.columns([1,1],gap='large')
with left:
    section("01","Tu boceto","Ratón o pantalla táctil")
    canvas=st_canvas(fill_color='rgba(255,138,76,0.25)',stroke_width=stroke,stroke_color='#000000',background_color='#FFFFFF',height=320,width=320,drawing_mode='freedraw',return_image_data=True,key='canvas')
    key=st.text_input("Clave de OpenAI",type='password')
    analyze=st.button("Interpretar boceto",type='primary')

has_drawing=bool(canvas.json_data and canvas.json_data.get('objects'))
png=None
if has_drawing and canvas.image_data is not None:
    image=Image.fromarray(np.asarray(canvas.image_data,dtype=np.uint8),'RGBA').convert('RGB')
    buffer=io.BytesIO(); image.save(buffer,format='PNG'); png=buffer.getvalue()
context=(hashlib.sha256(png).hexdigest() if png else None,hashlib.sha256(key.encode()).hexdigest())
if st.session_state.get('sketch_context') != context:
    st.session_state.pop('sketch_response',None)
    st.session_state.sketch_context=context

with right:
    section("02","Interpretación","Boceto → Lenguaje")
    if analyze:
        if not key:
            st.warning("Ingresa tu clave de OpenAI para continuar.")
        elif not png:
            st.warning("Dibuja un boceto antes de interpretarlo.")
        else:
            try:
                with st.spinner("Interpretando tu dibujo…"):
                    with OpenAI(api_key=key) as client:
                        response=client.chat.completions.create(model='gpt-4o-mini',max_tokens=500,messages=[{'role':'user','content':[{'type':'text','text':'Describe the image in spanish'},{'type':'image_url','image_url':{'url':'data:image/png;base64,'+base64.b64encode(png).decode()}}]}])
                    st.session_state.sketch_response=response.choices[0].message.content or 'El modelo no devolvió una descripción.'
            except Exception:
                st.error("No se pudo interpretar el boceto. Revisa la clave, el acceso al modelo y la conexión.")
    if st.session_state.get('sketch_response'):
        st.markdown(st.session_state.sketch_response)
    else:
        st.info("Tu interpretación aparecerá aquí cuando envíes un dibujo.")
footer("DIBUJAR / INTERPRETAR / CONTRASTAR")
