import streamlit as st
from Funciones_Oracle import Oracle
from impresion import imprimir_ticket

st.set_page_config(page_title='Tótem Médico', layout='centered')


conn_id='system/boca@XE'


st.markdown('''
<style>
header, footer, #MainMenu {display:none;}
.stApp {background:#edf3f8; color:#174c78;}
.block-container {max-width:850px; padding:2rem 1.5rem;}
h1,h2,h3 {text-align:center; color:#174c78;}
.stButton button {width:100%; min-height:100px; border:0;
 border-radius:16px; color:white; background:#1764a0;}
.stButton button p {font-size:clamp(22px,3vw,30px); font-weight:700;}
.stButton button:hover, .stButton button:focus {color:white; filter:brightness(.9);}
.st-key-turno button {background:#1764a0;}
.st-key-nuevo button {background:#168577;}
.st-key-tramites button {background:#526579;}
</style>
<div style="background:#174c78;color:white;text-align:center;padding:25px;border-radius:16px">
<div style="font-size:40px">🏥</div>
<div style="font-size:30px;font-weight:bold">CENTRO MÉDICO</div>
<div style="font-size:19px">Terminal de autogestión</div>
</div>
''', unsafe_allow_html=True)

if 'opcion' not in st.session_state:
    st.session_state.opcion = ''

def seleccionar(opcion):

    prefijos = {
        'Tengo turno': 'T',
        'Necesito un turno': 'N',
        'Otros trámites': 'A'
    }

    tipo_atencion = prefijos[opcion]
    
    cn = Oracle.Conexion(conn_id)
    cursor = cn.cursor()

    id_ticket = cursor.var(int)

    cursor.execute("""
        INSERT INTO TICKETS (TIPO_ATENCION)
        VALUES (:tipo)
        RETURNING ID_TICKET INTO :id_ticket
    """, tipo=tipo_atencion, id_ticket=id_ticket)

    # Recuperar ID generado
    id_generado = id_ticket.getvalue()[0]

    # Recuperar código de atención
    cursor.execute("""
        SELECT CODIGO_ATENCION
        FROM TICKETS
        WHERE ID_TICKET = :id 
        AND ESTADO='PENDIENTE'
    """, id=id_generado)

    codigo = cursor.fetchone()[0]


    cn.commit()

    st.session_state.codigo = codigo
    st.session_state.opcion = opcion

    cursor.close()
    cn.close()




if not st.session_state.opcion:
    st.header('¡Bienvenido!')
    st.subheader('¿En qué podemos ayudarlo?')
    st.button('📅 Tengo turno', key='turno', width='stretch', on_click=seleccionar, args=('Tengo turno',))
    st.button('➕ Necesito un turno', key='nuevo', width='stretch', on_click=seleccionar, args=('Necesito un turno',))
    st.button('📋 Otros trámites', key='tramites', width='stretch', on_click=seleccionar, args=('Otros trámites',))
    st.markdown('<p style="text-align:center;color:#526579;font-size:18px">Toque una opción para obtener su ticket</p>', unsafe_allow_html=True)
else:
    prefijos = {'Tengo turno':'T', 'Necesito un turno':'N', 'Otros trámites':'A'}
    st.header('¡Gracias!')
    st.subheader(st.session_state.opcion)

    st.title(st.session_state.codigo)
    st.caption('Ticket de demostración')
    st.info('Por favor, aguarde a ser llamado.')
    # TODO: Imprimir ticket térmico.

    if st.button('Imprimir Ticket',width='stretch'):
        try:
            imprimir_ticket(
                st.session_state.codigo,
                st.session_state.opcion
            )

            #st.success("Ticket enviado a la impresora")

        except Exception as e:
            st.error(f"Error de impresión: {e}")

    if st.button('Finalizar', width='stretch'):
        st.session_state.opcion = ''

        #cambiar pendiente por finalizar
        xupdate = Oracle.ExecuteOperation(conn_id,"update tickets set estado='FINALIZADO' Where estado='PENDIENTE'")

    


        st.rerun()
