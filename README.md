# **Image Resources - Progetto SDCC - Mazzola Alessio 0279323**

## **Abstract**

L'idea del progetto è quello di realizzare un'applicazione con architettura "mista" nella quale le funzioni di modifica delle immagini sono di natura serverless, mentre 
i rimanenti elementi dell'applicazione sono eseguiti attraverso un server Flask. Le funzioni che vengono esposte dall'applicativo sono le seguenti:

- **Resize:** Permette di eseguire il ridimensionamento di un'immagine;
- **Black&White:** Permette la trasformazione dell'immagine in Bianco e Nero;
- **Saturation:** Permette di eseguire la modifica della saturazione dell'immagine;
- **Brightness:** Permette di eseguire la modifica della luminosità dell'immagine.

Le funzioni appena menzionate rispettano il paradigma **Serverless**, sono infatti sviluppate sfruttando il servizio esposto da Amazon denominato **AWS Lambda**.

E' possibile utilizzare l'applicazione sia come utente **Guest** che come **Utente Registrato**. In particolare un Utente Registrato avrà a disposizione una ulteriore funzione che permetterà a quest'ultimo di visionare le immagini processate dall'applicazione in precedenza ed in caso permetterà nuovamente di scaricare queste ultime all'utente.

I servizio **Amazon AWS** utilizzati sono dunque i seguenti:
- **Cognito:** Necessario per registrazione e l'accesso degli utenti.
- **Api-Gateway:** Necessario per la comunicazione asincrona con le funzioni serverless.
- **S3:** Necessario per lo storage delle immagini degli utenti registrati.
- **Lambda:** Necessario per la creazione delle funzioni serverless.
- **DynamoDB:** Necessario per mantenere uno storico delle immagini processate dagli utenti.

## **Librerie Python utilizzate**

- **Flask (https://pypi.org/project/Flask/)**
  - Necessario per il web server della dashboard e gli endpoint per le chiamate REST.
- **Pillow (https://pypi.org/project/Pillow/)**
  - Necessario per la modifica delle immagini.
- **requests (https://pypi.org/project/requests/)**
  - Necessario per effettuare chiamate GET.
- **boto3 (https://pypi.org/project/boto3/)**
  - Necessario per la comunicazione con i servizi Amazon AWS.

## **Implementazione**

- Modulo **main.py:**
  - Modulo principale dell'applicazione. Si occupa dell'avvio del server Flusk e contiene al suo interno tutte le funzioni di redirezione e di esecuzione dell'applicativo.
  - ***doBeW():*** Funzione adibita alla modifica di un immagine rendendola Bianco e Nero. (Tramite la libreria Redirect si va a richiamare la rest-api creata attraverso il servizio Api Gateway)
  - ***doResize()*** Funzione che esegue il ridimensionamento dell'immagine. (Tramite la libreria Redirect si va a richiamare la rest-api creata attraverso il servizio Api Gateway)
  - ***doBrightness()*** Funzione per la modifica della luminosità dell'immagine. (Tramite la libreria Redirect si va a richiamare la rest-api creata attraverso il servizio Api Gateway)
  - ***doSaturation()*** Funzione per la modifica della saturazione dell'immagine. (Tramite la libreria Redirect si va a richiamare la rest-api creata attraverso il servizio Api Gateway)  
  - ***doListTable()*** Funzione utilizzata per andare a popolare la tabella delle immagini già processate in precedenza dall'utente.
  - ***doDownloadFromUrl()*** Funzione utilizzata per eseguire il download dell'immagine presente all'interno del Bucket S3.

- Modulo **functionCognito.py:** 
  - Questo modulo presenta al suo interno le funzioni utilizzate per interfacciarsi con il servizio **AWS Cognito**, in particolare sono state sviluppati i seguenti metodi:
    - ***register_user()*** Funzione adibita alla registrazione dell'utente all'interno dell'applicazione.
    - ***accedi_user()*** Funzione adibita al controllo delle credenziali dell'utente una volta che questo tenta di eseguire l'accesso.

- Modulo **functionDynamo.py:** 
  - Questo modulo presenta al suo interno le funzioni utilizzate per interfacciarsi con il servizio **AWS DynamoDB**, in particolare sono state sviluppati i seguenti metodi:
    - ***add_element_in_table(...)*** Funzione adibita all'inserimento dell'elemento all'interno della tabella specificata.
    - ***get_element_from_table(...)*** Funzione adibita al recupero di un determinato elemento dalla specifica tabella.

- Modulo **functionS3.py:** 
  - Questo modulo presenta al suo interno le funzioni utilizzate per interfacciarsi con il servizio **AWS DynamoDB**, in particolare sono state sviluppati i seguenti metodi:
    - ***addToBucket(...)*** Funzione adibita all'inserimento dell'elemento all'interno dello specifico BucketS3.
    - ***removeFromBucket(...)*** Funzione adibita all'eliminazione di un determinato elemento presente all'interno del BucketS3.
    - ***donwloadFromBucket(...)*** Funzione adibita al download dell'elemento specifico presente all'interno del BucketS3.

- Modulo **ConfigS3.py:** 
  - Questo modulo presenta al suo interno delle stringhe specifiche per la configurazione dei servizi AWS utilizzati. In particolare è necessario fornire i *Token* generati ad ogni sessione (Presenti nel portale **Vocareum**). Sono inoltre specificati all'interno i nomi dei Bucket per le diverse funzioni e l'*identity pool* necessario al funzionamento del servizio di **AWS Cognito**.

# **Image Resources - Setup**

## **Avvio cluster**

0. **Installazione delle dipendenze necessarie;**
1. **Update delle chiavi di sessione all'interno del file ConfigS3;**
2. **Upadte delle funzioni Lambda;**
   1. Al loro interno dovranno essere aggiornate le chiavi della sessione.
3. **Avvio del server Flusk;**
   1. ```sudo python3 main.py``` (I privilegi *sudo* sono necessari se viene utilizzata una macchina EC2)

## **Link Utili**

  - **Documentazione DynamoDB:** https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
  - **Documentazione Cognito:** https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.sign_up
  - **Documentazione S3:** https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html

## **Limitazioni riscontrate**

Durante lo sviluppo dell'applicazione sono stati riscontrate alcune limitazioni dovute all'utilizzo dell'account **Educate** per AWS. La limitazione più grande è stata
**L'impossibilità di creazione di utenti IAM:** Questa è stata la limitazione più grande, in quanto la creazione di account IAM avrebbe permesso di creare account con determinati permessi, in modo da non dover modificare ogni tot tempo le chiavi della sessione, pregiudicandone quindi l'utizzo dei servizi di AutoScaling e del LoadBalancer.