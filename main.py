import streamlit as st
import streamlit_authenticator as stauth
from dependencies import consulta_nome, consulta_geral, add_registro, criar_tabela
from time import sleep

COOKIE_EXPIRE_DAYS =  30


def main():
    db_query = []
    try:                
        db_query = consulta_geral()
    except:  
        criar_tabela()

    # cria um dicionario dos registros existentes.
    registros = {'usernames': {}}  
    for data in db_query:
        # db_query returns lists with each index from the table inside a tuple. 
        # for each information on the tuples we can turn it all into a dictionary for the authenticator
        registros['usernames'][data[1]] = {'name': data[0], 'password': data[2]}    


    authenticator = stauth.Authenticate(
        registros ,
        'random_cookie_name'  ,
        'random_signature_key',
        COOKIE_EXPIRE_DAYS    , 
    )
    if 'isRegistring' not in st.session_state   :
        st.session_state['isRegistring'] = False
    if st.session_state['isRegistring'] == False:
        login_form(authenticator=authenticator)
        Button('registrar', onRegister)
    else:
        registerForm()
        Button("Voltar", onShowLoginForm)     


def Button(text, onClick): 
    ''' Create a button and activate it. '''
    if st.button(text):
        onClick()
   
def onRegister():
    ''' function responsable with turning 'isRegistring'variable into True '''
    st.session_state['isRegistring'] = True     
    st.rerun()                                  
   
def onShowLoginForm():  
    ''' function responsable with turning 'isRegistring'variable into False '''
    st.session_state['isRegistring'] = False   
    st.rerun()                                 



def login_form(authenticator):
    name, authentication_status, username = authenticator.login('Login')    
    # this is the place to put the files and informations that are secured by the password. 
    if authentication_status:
        authenticator.logout('Logout', 'main')                               
        st.title('Area do Dashboard')                                        
        st.write(f'*{name} está logado(a)!')                                
    # login error
    elif authentication_status == False:                                    
        st.error('Usuario/senha incorretos')
    # attempt to login without any information
    elif authentication_status == None:                                     
        st.warning('Por favor informe um usuário e senha')


def registerForm(): 
    ''' Function responsable with the form, just the form, for a new user creation  '''
    with  st.form(key="Formulario", clear_on_submit=True):    
        nome     = st.text_input(label="Nome",     key = "nome", placeholder='Placeholder serve para escrever o texto aq.')
        username = st.text_input(label="username", key = "user", placeholder='Placeholder serve para escrever o texto aq.')
        password = st.text_input(label="password", key = "pswrd", type='password',  placeholder='Placeholder serve para escrever o texto aq.')
        confirm_password = st.text_input(label="confirme password", type='password', key = "confirm_pswrd", placeholder='Placeholder serve para escrever o texto aq.')
        submit   = st.form_submit_button(     
            "Salvar", on_click= userCreation,   
        ) 


def userCreation():
    ''' Responsable with the verification if the information placed already exists and if not, create the new user'''
    hashed_password = stauth.Hasher([st.session_state.pswrd]).generate()   
    if consulta_nome(st.session_state.user):
        st.warning('Nome de usuario já existe')
        sleep (3)
    elif st.session_state.pswrd != st.session_state.confirm_pswrd:
        st.warning('Senhas não conferem.')
        sleep (3)
    else: 
        add_registro(st.session_state.nome, st.session_state.user, hashed_password[0])
        st.success('Registro efetuado')
        sleep (3)



if __name__ == '__main__':
    main()