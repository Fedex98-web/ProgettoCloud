

# cloud function Punto 2
def save_data_1_bq(request):
    from google.cloud import bigquery
    from datetime import datetime, timedelta
    client = bigquery.Client()
    project_id = 'gnocchi-test-415019'
    dataset_id = 'test1'
    table_id = 'tabtesina'
    table_full_id = f'{project_id}.{dataset_id}.{table_id}'

    request_json = request.get_json(silent=True)
    if request_json:
        sensor = request_json['sensor']
        dt = request_json['tempo']
        valori = request_json['valori']
        stringhe = request_json['stringhe']
        rows = [{'sensor': sensor, 'datetime': dt, 'valori': valori, 'stringhe': stringhe}]
        errors = client.insert_rows_json(table_full_id, rows)  # Make an API request.
        if errors == []:
            return "New rows have been added."
        else:
            return "Encountered errors while inserting rows: {}".format(errors)


# cloud function Punto 3
d = []
d.append(['datetime', 'dati'])
def graph_data(request):
    from datetime import datetime
    from flask import render_template
    request_json = request.get_json(silent=True)
    if request_json:
        sensor = request_json['sensor']
        valori = request_json['valori']
        dt = datetime.fromtimestamp(request_json['tempo'])
        d.append([str(dt), sum(valori)])
        return render_template('graph.html', sensor=sensor, data=d)


# cloud function Punto 4
def send_email():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from secret import pw
    # Parametri per la connessione SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Porta SMTP di Gmail
    sender_email = 'gnocchifederico49@gmail.com'
    sender_password = pw
    # Informazioni sull'email
    receiver_email = 'gnocchifederico49@gmail.com'
    subject = 'Ricezione anomalia'
    body = 'E\' stato ricevuto un valore anomalo'
    # Creazione del messaggio
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    # Aggiunta del corpo del messaggio
    message.attach(MIMEText(body, 'plain'))
    # Connessione al server SMTP di Gmail
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Avvia il protocollo TLS per la sicurezza
    # Login al server SMTP
    server.login(sender_email, sender_password)
    # Invio dell'email
    server.sendmail(sender_email, receiver_email, message.as_string())
    # Chiudi la connessione SMTP
    server.quit()
    print('Email sent successfully!')



def detect_anomalies(request):
    request_json = request.get_json(silent=True)
    if request_json:
        val = request_json['valori']
        for x in val:
            if x > 100:
                print('Valore anomalo: {}'.format(x))
                send_email()
            else:
                print('Ok: {}'.format(x))
    return "Function executed successfully!"


