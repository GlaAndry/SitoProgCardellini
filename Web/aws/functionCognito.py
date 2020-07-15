import boto3
from botocore.client import Config


#Questo file è adibito alla creazione di funzioni per la web app grazie a cognito

def register_user_admin(userName,email,password, UserPoolId, cognito):
    ##Questa funzione registra un utente all'interno di cognito e lo accetta.
    
        response = cognito.admin_create_user(
        UserPoolId='us-east-1_weYuVbI38',
        Username=userName,
        UserAttributes=[
        {
            'Name': "name",
            'Value': userName
        },
        {
            'Name': "email",
            'Value': email
        }
        ],
        ValidationData=[
            {
            'Name': "email",
            'Value': email
        },
        {
            'Name': "custom:username",
            'Value': userName
        }],

        TemporaryPassword = password
        )
    
        #abilito l'utente
        response = cognito.admin_enable_user(
            UserPoolId='us-east-1_weYuVbI38',
            Username=userName
        )

def register_user(userName,email,password, clientID, cognito):
    #Questa funzione permette l'accesso dell'utente all'interno del sistema.
    response = cognito.sign_up(
    ClientId=clientID,
    #SecretHash='1klluajjauvgnped20vnt51ikuu86g7nr2jlacht7kg2trb8bqrd', ##da modificare ogni 30 giorni
    ##si trova tutto in cognito --> clienti dell'app (espandere opzioni)
    Username=userName,
    Password=password,
    UserAttributes=[
    {
        'Name': "name",
        'Value': userName
    },
    {
        'Name': "email",
        'Value': email
    }
    ],
    ValidationData=[
        {
        'Name': "email",
        'Value': email
    },
    {
        'Name': "custom:username",
        'Value': userName
    }],
    )

def accedi_user(clientID, email, password, cognito):
    ##Questo metodo si occupa di verificare che le credenziali inserite 
    ##siano correte, restituendo un token di accesso
    response = cognito.initiate_auth(
            ClientId=clientID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={'USERNAME': email, 'PASSWORD': password }
    )