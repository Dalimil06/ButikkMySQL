import mysql.connector # Importerer mysql connector for å ha det nødvendige for å kunne koble til databasen min

host = '10.148.67.56' # IP-adressen til serveren
user = 'python' # Navnet på brukeren
password = 'Romsdal Vgs 2024' # Passordet på brukeren
database = 'bord_butikk' # Databasen som blir brukt


def sql(sql_string): # Lager en sql funksjon
    query = sql_string
    cursor.execute(query)
    output = cursor.fetchall()
    return output


def login(): # Lager en login funksjon for å lage bruker, eller til å logge på for å få tilgang til butikken
    global fornavn, etternavn, signedIn
    print("1: Login")
    print("2: Lag bruker")
    login = str.lower(input("Hva vil du gjøre?"))

    if login == "2" or login == "lag bruker": # Hvis du velger å lage en ny bruker
        fornavn = input("Skriv inn ditt fornavn:")
        etternavn = input("Skriv inn ditt etternavn:")
        email = input("Skriv inn email-adressen din:")
        mobilnr = input("Skriv inn ditt mobilnummer:")
        postnr = input("Skriv inn ditt postnummer:")
        adresse = input("Skriv inn adressen din:")
        sql(f'INSERT INTO kunde (fornavn, etternavn, email, mobilnr, postnr, adresse) VALUES ({fornavn},{etternavn},{email},{mobilnr},{postnr},{adresse});')
        signedIn = True # Variable for å registre om du er pålogget

    elif login == "1" or login == "login": # Hvis du velger å logge inn
        print()
        fornavn = str.lower(input("Skriv inn ditt fornavn"))
        etternavn = str.lower(input("Skriv inn ditt etternavn"))
            # Sjekker om brukeren finnes
        if sql(f'SELECT fornavn FROM kunde WHERE fornavn {fornavn}') == fornavn and sql(f'SELECT etternavn FROM kunde WHERE etternavn {etternavn}') == etternavn:
            print("Du er nå logget på")
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
    print(sql("SELECT * FROM produkt")) # Viser alle produkter

    skal_kjope = str.lower(input("Ønsker du å kjøpe et produkt? (ja/nei)"))
    if skal_kjope == "ja":
        vare_kjop = str.lower(input("Hva produkt ønsker du å kjøpe:"))
        print(sql(f'SELECT * FROM produkt WHERE produktnavn {vare_kjop}')) # Viser det produktet som kunden ønsker å kjøpe
        antall = str.lower(input("Hvor mange ønsker du å kjøpe:")) # Spør om antall kunden ønsker å kjøpe

        er_sikker = str.lower(input("Er du sikker på at du vil kjøpe dette produktet?")) # Sjekker om kunden ønsker å kjøpe produktet
        if er_sikker == "ja":
            sql(f'UPDATE produkt SET antall = antall {antall}') # Oppdaterer antallet etter antall kjøpte produkt
            kundeID = sql(f'SELECT kundeID FROM kunde WHERE fornavn {fornavn} and etternavn {etternavn}') # Finner ID-en til kunden
            sql(f'INSERT INTO kjop (kundeID) VALUES {kundeID}') # Registrerer ID-en til kunden
            print(sql('SELECT BOTTOM 1 * FROM kjop')) # Viser kjøpet og all informasjon om det
            print("Takk for kjopet")

        elif er_sikker == "nei": # Hvis du ombestemmer deg
            print("Kjøpet ble avbrutt!")
    
    else:
        print()


def kjop(): # Funksjon for å vise alle tidligere kjøp fra brukeren
    fornavn = "Emma"
    etternavn = "Jensen"
    kundeID = sql(f'SELECT kundeID FROM kunde WHERE fornavn {fornavn} and etternavn {etternavn}') # Finner ID-en til brukeren
    print("Her er dine tidligere kjøp:")
    print(sql(f'SELECT * FROM kjop WHERE kundeID {kundeID}')) # Viser alle registrerte kjøp fra den brukeren
    input("Trykk ENTER for å gå tilbake til menyen:")


#Main
try: # Kobler til Serveren med Databasen
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected(): # Sjekker om koblingen lykkes
        print("Connected to the database!")
        cursor = connection.cursor()
        
        valg = "9"
        signedIn = False

       # while signedIn == False: # Sjekker om du er logget på
        #    login() # Kjører påloggingsfunskjonen

        while valg != "0": # Sjekker hva valg du har valgt
            if valg == "1": # Om du ønsker å vise alle kunder
                print(sql("SELECT * FROM kunde;"))
                
            elif valg == "2": # For visning og kjøp av produkt
                produkt()
                
            elif valg == "3": # For visning av tidligere kjøp
                kjop()

            valg = "9"
            meny() # Kjører meny funskjonen for hver gang så lenge valget ikke er 0 (Avslutt)

except mysql.connector.Error as err: # Hvis det oppstår en feil
    print(f"Error: {err}")

finally: # Avslutter connection etter at programet avsluttes
    if 'connection' in locals():
        connection.close()
        print("Connection closed.")

cursor.close()
connection.close()