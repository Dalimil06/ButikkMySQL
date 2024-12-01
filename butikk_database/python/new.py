import mysql.connector # Importerer mysql connector for å ha det nødvendige for å kunne koble til databasen min

butikkDB = mysql.connector.connect(
    host = "10.148.67.56",
    user = "python", # Navnet på brukeren
    password = "Romsdal Vgs 2024", # Passordet på brukeren
    database = "bord_butikk", # Databasen som blir brukt
)

mycursor = butikkDB.cursor()

def login(): # Lager en login funksjon for å lage bruker, eller til å logge på for å få tilgang til butikken
    global fornavn, etternavn, signedIn
    print("1: Login")
    print("2: Lag bruker")
    login = str.lower(input("Hva vil du gjøre?"))

    if login == "2" or login == "lag bruker": # Hvis du velger å lage en ny bruker
        fornavn = input("Skriv inn ditt fornavn:")
        etternavn = input("Skriv inn ditt etternavn: ")
        email = input("Skriv inn email-adressen din: ")
        mobilnr = input("Skriv inn ditt mobilnummer: ")
        postnr = input("Skriv inn ditt postnummer: ")
        adresse = input("Skriv inn adressen din: ")
        sql = "INSERT INTO kunde (fornavn, etternavn, email, mobilnr, postnr, adresse) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (fornavn, etternavn, email, mobilnr, postnr, adresse)
        mycursor.execute(sql, val)

        butikkDB.commit()
        signedIn = True # Variable for å registre om du er pålogget


    elif login == "1" or login == "login": # Hvis du velger å logge inn
        print()
        fornavn = input("Skriv inn ditt fornavn: ")
        etternavn = input("Skriv inn ditt etternavn: ")
            # Sjekker om brukeren finnes
        mycursor.execute(f"SELECT fornavn FROM kunde WHERE fornavn = '{fornavn}'")
        fornavnDB = mycursor.fetchone()
        mycursor.execute(f"SELECT etternavn FROM kunde WHERE etternavn = '{etternavn}'")
        etternavnDB = mycursor.fetchone()
    
        if fornavn == fornavnDB[0] and etternavn == etternavnDB[0]:
            print(f"Du er nå logget på som: {fornavn} {etternavn}")
            signedIn = True 

        else: # Hvis brukeren ikke finnes
            print("Denne brukeren finnes ikke!")
            signedIn = False
        
    else: # Hvis det oppstår en feil ved innlogging
        print("Det oppstod en feil ved pålogging!")
        signedIn = False

    return signedIn, fornavn, etternavn



def meny(): # Lager en meny funskjon
    global valg
    print()
    print("_____________________")
    print("1: Vis alle brukere")
    print("2: Vis alle produkter")
    print("3: Vis mine kjøp")
    print("_____________________")
    print("0: Avslutt")
    print("_____________________")
    valg = str.lower(input("Hva vil du gjøre:"))
    return valg


def produkt(): # Lager en funskjon for å vise alle produkter og kjøp
    mycursor.execute("SELECT * FROM produkt")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

    skal_kjope = str.lower(input("Ønsker du å kjøpe et produkt? (ja/nei)"))
    if skal_kjope == "ja":
        vare_kjop = input("Hva produkt ønsker du å kjøpe:")

        sql = f"SELECT * FROM produkt WHERE produktnavn = '{vare_kjop}'"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)

        antall = str.lower(input("Hvor mange ønsker du å kjøpe:")) # Spør om antall kunden ønsker å kjøpe
        er_sikker = str.lower(input("Er du sikker på at du vil kjøpe dette produktet?")) # Sjekker om kunden ønsker å kjøpe produktet
        if er_sikker == "ja":
            sql = f"SELECT produktID FROM produkt WHERE produktnavn = '{vare_kjop}'"
            mycursor.execute(sql)
            produktID = mycursor.fetchall()
            sql = f"INSERT INTO kjop (produktID) VALUES '{produktID}'"
            mycursor.execute(sql)

            sql = f"UPDATE produkt SET antall = antall -'{antall}'" # Oppdaterer antallet etter antall kjøpte produkt
            mycursor.execute(sql)
            sql = f"INSERT INTO kjop (antall_kjopt) VALUES '{antall}'"
            mycursor.execute(sql)

            sql = f"SELECT pris FROM produkt WHERE produktID = '{produktID}'"
            mycursor.execute(sql)
            pris = mycursor.fetchall()
            pris = pris * antall
            sql = f"INSERT INTO kjop (totalpris) VALUES '{pris}'"

            sql = f"SELECT kundeID FROM kunde WHERE fornavn = '{fornavn}' AND etternavn = '{etternavn}'"
            mycursor.execute(sql)
            kundeID = mycursor.fetchall()
            sql = f"INSERT INTO kjop (kundeID) VALUES '{kundeID}'"
            mycursor.execute(sql)

            print("Takk for kjopet")

        elif er_sikker == "nei": # Hvis du ombestemmer deg
            print("Kjøpet ble avbrutt!")
    
    else:
        print()


def kjop(): # Funksjon for å vise alle tidligere kjøp fra brukeren
    sql = f"SELECT kundeID FROM kunde WHERE fornavn = '{fornavn}' AND etternavn = '{etternavn}'"
    mycursor.execute(sql)
    kundeID = mycursor.fetchall()
    # Finner ID-en til brukeren
    print("Her er dine tidligere kjøp:")
     # Viser alle registrerte kjøp fra den brukeren
    sql = f"SELECT * FROM kjop WHERE kundeID = '{kundeID}'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if not myresult:
        print("Ingen tidligere kjøp")
    for x in myresult:
        print(x)
        
    input("Trykk ENTER for å gå tilbake til menyen")


#Main
# Kobler til Serveren med Databasen

valg = "9"
signedIn = False

while not signedIn: # Sjekker om du er logget på
    login() # Kjører påloggingsfunskjonen

while valg != "0": # Sjekker hva valg du har valgt
    if valg == "1": # Om du ønsker å vise alle kunder
        mycursor.execute("SELECT * FROM kunde")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
        
    elif valg == "2": # For visning og kjøp av produkt
        produkt()
        
    elif valg == "3": # For visning av tidligere kjøp
        kjop()

    valg = "9"
    meny() # Kjører meny funskjonen for hver gang så lenge valget ikke er 0 (Avslutt)