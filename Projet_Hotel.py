import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date
import os

# Configuration de la page
st.set_page_config(
    page_title="Gestion Hôtel",
    page_icon="🏨",
    layout="centered"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour initialiser la base de données SQLite
def init_database():
    """Initialise la base de données SQLite avec les tables et données"""
    conn = sqlite3.connect('hotel_reservation.db')
    cursor = conn.cursor()
    
    # Création des tables
    cursor.executescript('''
    -- Table Hotel
    CREATE TABLE IF NOT EXISTS Hotel (
        id_hotel INTEGER PRIMARY KEY,
        ville TEXT NOT NULL,
        pays TEXT NOT NULL,
        code_postal TEXT
    );

    -- Table Client
    CREATE TABLE IF NOT EXISTS Client (
        id_client INTEGER PRIMARY KEY,
        adresse TEXT,
        ville TEXT,
        code_postal TEXT,
        email TEXT,
        telephone TEXT,
        nom TEXT NOT NULL
    );

    -- Table Prestation
    CREATE TABLE IF NOT EXISTS Prestation (
        id_prestation INTEGER PRIMARY KEY,
        prix REAL,
        nom TEXT NOT NULL
    );

    -- Table Type_Chambre
    CREATE TABLE IF NOT EXISTS Type_Chambre (
        id_type INTEGER PRIMARY KEY,
        nom TEXT NOT NULL,
        prix REAL NOT NULL
    );

    -- Table Chambre
    CREATE TABLE IF NOT EXISTS Chambre (
        id_chambre INTEGER PRIMARY KEY,
        numero INTEGER NOT NULL,
        etage INTEGER,
        balcon BOOLEAN DEFAULT 0,
        id_hotel INTEGER,
        id_type INTEGER,
        FOREIGN KEY (id_hotel) REFERENCES Hotel(id_hotel),
        FOREIGN KEY (id_type) REFERENCES Type_Chambre(id_type)
    );

    -- Table Reservation
    CREATE TABLE IF NOT EXISTS Reservation (
        id_reservation INTEGER PRIMARY KEY,
        date_debut DATE NOT NULL,
        date_fin DATE NOT NULL,
        id_client INTEGER,
        FOREIGN KEY (id_client) REFERENCES Client(id_client)
    );

    -- Table Evaluation
    CREATE TABLE IF NOT EXISTS Evaluation (
        id_evaluation INTEGER PRIMARY KEY,
        date_evaluation DATE,
        note INTEGER CHECK (note >= 1 AND note <= 5),
        commentaire TEXT,
        id_reservation INTEGER,
        FOREIGN KEY (id_reservation) REFERENCES Reservation(id_reservation)
    );

    -- Table de liaison Reservation_Chambre
    CREATE TABLE IF NOT EXISTS Reservation_Chambre (
        id_reservation INTEGER,
        id_chambre INTEGER,
        PRIMARY KEY (id_reservation, id_chambre),
        FOREIGN KEY (id_reservation) REFERENCES Reservation(id_reservation),
        FOREIGN KEY (id_chambre) REFERENCES Chambre(id_chambre)
    );
    ''')
    
    # Vérifier si les données existent déjà
    cursor.execute("SELECT COUNT(*) FROM Hotel")
    if cursor.fetchone()[0] == 0:
        # Insertion des données initiales
        cursor.executescript('''
        -- Données Hotel
        INSERT INTO Hotel VALUES 
        (1, 'Paris', 'France', '75001'),
        (2, 'Lyon', 'France', '69002');

        -- Données Client
        INSERT INTO Client VALUES 
        (1, '12 Rue de Paris', 'Paris', '75001', 'jean.dupont@email.fr', '0612345678', 'Jean Dupont'),
        (2, '5 Avenue Victor Hugo', 'Lyon', '69002', 'marie.leroy@email.fr', '0623456789', 'Marie Leroy'),
        (3, '8 Boulevard Saint-Michel', 'Marseille', '13005', 'paul.moreau@email.fr', '0634567890', 'Paul Moreau'),
        (4, '27 Rue Nationale', 'Lille', '59800', 'lucie.martin@email.fr', '0645678901', 'Lucie Martin'),
        (5, '3 Rue des Fleurs', 'Nice', '06000', 'emma.giraud@email.fr', '0656789012', 'Emma Giraud');

        -- Données Prestation
        INSERT INTO Prestation VALUES 
        (1, 15.00, 'Petit-déjeuner'),
        (2, 30.00, 'Navette aéroport'),
        (3, 0.00, 'Wi-Fi gratuit'),
        (4, 50.00, 'Spa et bien-être'),
        (5, 20.00, 'Parking sécurisé');

        -- Données Type_Chambre
        INSERT INTO Type_Chambre VALUES 
        (1, 'Simple', 80.00),
        (2, 'Double', 120.00);

        -- Données Chambre
        INSERT INTO Chambre VALUES 
        (1, 201, 2, 0, 1, 1),
        (2, 502, 5, 1, 1, 2),
        (3, 305, 3, 0, 2, 1),
        (4, 410, 4, 0, 2, 2),
        (5, 104, 1, 1, 2, 2),
        (6, 202, 2, 0, 1, 1),
        (7, 307, 3, 1, 1, 2),
        (8, 101, 1, 0, 1, 1);

        -- Données Reservation
        INSERT INTO Reservation VALUES 
        (1, '2025-06-15', '2025-06-18', 1),
        (2, '2025-07-01', '2025-07-05', 2),
        (3, '2025-08-10', '2025-08-14', 3),
        (4, '2025-09-05', '2025-09-07', 4),
        (5, '2025-09-20', '2025-09-25', 5),
        (7, '2025-11-12', '2025-11-14', 2),
        (9, '2026-01-15', '2026-01-18', 4),
        (10, '2026-02-01', '2026-02-05', 2);

        -- Liaison Reservation-Chambre
        INSERT INTO Reservation_Chambre VALUES 
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
        (7, 7), (9, 4), (10, 2);

        -- Données Evaluation
        INSERT INTO Evaluation VALUES 
        (1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1),
        (2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2),
        (3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3),
        (4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4),
        (5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5);
        ''')
    
    conn.commit()
    conn.close()

# Fonction pour obtenir la connexion à la base
def get_connection():
    return sqlite3.connect('hotel_reservation.db')

# Fonctions de base de données
def get_reservations():
    conn = get_connection()
    query = '''
    SELECT 
        r.id_reservation as "ID",
        c.nom as "Client",
        h.ville as "Ville",
        r.date_debut as "Arrivée",
        r.date_fin as "Départ",
        ch.numero as "Chambre",
        tc.nom as "Type"
    FROM Reservation r
    JOIN Client c ON r.id_client = c.id_client
    JOIN Reservation_Chambre rc ON r.id_reservation = rc.id_reservation
    JOIN Chambre ch ON rc.id_chambre = ch.id_chambre
    JOIN Hotel h ON ch.id_hotel = h.id_hotel
    JOIN Type_Chambre tc ON ch.id_type = tc.id_type
    ORDER BY r.date_debut DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_clients():
    conn = get_connection()
    query = 'SELECT id_client as "ID", nom as "Nom", email as "Email", telephone as "Téléphone", ville as "Ville" FROM Client ORDER BY nom'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def add_client(nom, email, telephone, ville, adresse="", code_postal=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id_client) FROM Client")
    max_id = cursor.fetchone()[0] or 0
    new_id = max_id + 1
    
    cursor.execute('''
    INSERT INTO Client (id_client, nom, adresse, ville, code_postal, email, telephone)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (new_id, nom, adresse, ville, code_postal, email, telephone))
    
    conn.commit()
    conn.close()
    return new_id

def get_available_rooms(date_debut, date_fin):
    conn = get_connection()
    query = '''
    SELECT 
        ch.id_chambre,
        ch.numero as "Chambre",
        h.ville as "Hôtel",
        tc.nom as "Type",
        tc.prix as "Prix/nuit",
        CASE WHEN ch.balcon = 1 THEN 'Oui' ELSE 'Non' END as "Balcon"
    FROM Chambre ch
    JOIN Hotel h ON ch.id_hotel = h.id_hotel
    JOIN Type_Chambre tc ON ch.id_type = tc.id_type
    WHERE ch.id_chambre NOT IN (
        SELECT DISTINCT rc.id_chambre
        FROM Reservation_Chambre rc
        JOIN Reservation r ON rc.id_reservation = r.id_reservation
        WHERE (r.date_debut <= ? AND r.date_fin >= ?)
    )
    ORDER BY h.ville, ch.numero
    '''
    df = pd.read_sql_query(query, conn, params=(date_fin, date_debut))
    conn.close()
    return df

def add_reservation(date_debut, date_fin, id_client, id_chambre):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT MAX(id_reservation) FROM Reservation")
    max_id = cursor.fetchone()[0] or 0
    new_id = max_id + 1
    
    cursor.execute('''
    INSERT INTO Reservation (id_reservation, date_debut, date_fin, id_client)
    VALUES (?, ?, ?, ?)
    ''', (new_id, date_debut, date_fin, id_client))
    
    cursor.execute('''
    INSERT INTO Reservation_Chambre (id_reservation, id_chambre)
    VALUES (?, ?)
    ''', (new_id, id_chambre))
    
    conn.commit()
    conn.close()
    return new_id

# Initialiser la base de données
init_database()

# Interface principale
st.markdown('<h1 class="main-header">🏨 Gestion Hôtel</h1>', unsafe_allow_html=True)

# Onglets simples
tab1, tab2, tab3, tab4 = st.tabs(["📊 Tableau de bord", "📋 Réservations", "👥 Clients", "➕ Nouvelle réservation"])

with tab1:
    st.header("Tableau de bord")
    
    # Métriques
    col1, col2, col3 = st.columns(3)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    with col1:
        cursor.execute("SELECT COUNT(*) FROM Reservation")
        nb_reservations = cursor.fetchone()[0]
        st.metric("Réservations totales", nb_reservations, delta="↗️")
    
    with col2:
        cursor.execute("SELECT COUNT(*) FROM Client")
        nb_clients = cursor.fetchone()[0]
        st.metric("Clients", nb_clients, delta="👥")
    
    with col3:
        cursor.execute("SELECT COUNT(*) FROM Chambre")
        nb_chambres = cursor.fetchone()[0]
        st.metric("Chambres", nb_chambres, delta="🏠")
    
    conn.close()
    
    # Dernières réservations
    st.subheader("Dernières réservations")
    df_recent = get_reservations().head(5)
    if not df_recent.empty:
        st.dataframe(df_recent, use_container_width=True, hide_index=True)
    else:
        st.info("Aucune réservation")

with tab2:
    st.header("Toutes les réservations")
    
    # Filtres simples
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Actualiser"):
            st.rerun()
    with col2:
        search_client = st.text_input("Rechercher un client", placeholder="Nom du client...")
    
    df_reservations = get_reservations()
    
    # Filtrage par nom de client
    if search_client:
        df_reservations = df_reservations[df_reservations['Client'].str.contains(search_client, case=False, na=False)]
    
    if not df_reservations.empty:
        st.dataframe(df_reservations, use_container_width=True, hide_index=True)
        st.info(f"Total: {len(df_reservations)} réservation(s)")
    else:
        st.info("Aucune réservation trouvée")

with tab3:
    st.header("Gestion des clients")
    
    # Sous-onglets pour clients
    subtab1, subtab2 = st.tabs(["Liste des clients", "Ajouter un client"])
    
    with subtab1:
        df_clients = get_clients()
        if not df_clients.empty:
            st.dataframe(df_clients, use_container_width=True, hide_index=True)
            st.info(f"Total: {len(df_clients)} client(s)")
        else:
            st.info("Aucun client")
    
    with subtab2:
        st.subheader("Nouveau client")
        
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom complet *", placeholder="Jean Dupont")
            email = st.text_input("Email", placeholder="jean@email.com")
        with col2:
            telephone = st.text_input("Téléphone", placeholder="0123456789")
            ville = st.text_input("Ville", placeholder="Paris")
        
        if st.button("➕ Ajouter le client", type="primary"):
            if nom:
                try:
                    new_id = add_client(nom, email, telephone, ville)
                    st.success(f"✅ Client ajouté ! ID: {new_id}")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erreur: {str(e)}")
            else:
                st.error("Le nom est obligatoire")

with tab4:
    st.header("Nouvelle réservation")
    
    # Étape 1: Dates et recherche
    st.subheader("1. Choisir les dates")
    col1, col2 = st.columns(2)
    with col1:
        date_debut = st.date_input("Date d'arrivée", value=date.today())
    with col2:
        date_fin = st.date_input("Date de départ", value=date.today())
    
    if date_debut >= date_fin:
        st.error("La date de départ doit être après l'arrivée")
    else:
        # Recherche de chambres
        if st.button("🔍 Chercher les chambres disponibles", type="primary"):
            df_available = get_available_rooms(date_debut.strftime('%Y-%m-%d'), date_fin.strftime('%Y-%m-%d'))
            
            if not df_available.empty:
                st.session_state['available_rooms'] = df_available
                st.session_state['dates'] = (date_debut, date_fin)
                st.success(f"✅ {len(df_available)} chambre(s) disponible(s)")
            else:
                st.warning("Aucune chambre disponible")
                st.session_state['available_rooms'] = pd.DataFrame()
        
        # Étape 2: Sélection chambre et client
        if 'available_rooms' in st.session_state and not st.session_state['available_rooms'].empty:
            st.subheader("2. Sélectionner une chambre")
            df_available = st.session_state['available_rooms']
            
            # Affichage des chambres disponibles
            st.dataframe(df_available.drop('id_chambre', axis=1), use_container_width=True, hide_index=True)
            
            # Sélection de chambre
            room_options = {}
            for _, row in df_available.iterrows():
                label = f"Chambre {row['Chambre']} - {row['Type']} - {row['Hôtel']} ({row['Prix/nuit']}€/nuit)"
                room_options[label] = row['id_chambre']
            
            selected_room = st.selectbox("Choisir une chambre", list(room_options.keys()))
            id_chambre = room_options[selected_room]
            
            st.subheader("3. Sélectionner le client")
            
            # Liste des clients
            df_clients = get_clients()
            if df_clients.empty:
                st.warning("Aucun client. Ajoutez d'abord un client dans l'onglet Clients.")
            else:
                client_options = {}
                for _, row in df_clients.iterrows():
                    label = f"{row['Nom']} - {row['Email']}"
                    client_options[label] = row['ID']
                
                selected_client = st.selectbox("Choisir un client", list(client_options.keys()))
                id_client = client_options[selected_client]
                
                # Récapitulatif
                st.subheader("4. Récapitulatif")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Client:** {selected_client.split(' - ')[0]}")
                    st.write(f"**Arrivée:** {date_debut}")
                    st.write(f"**Départ:** {date_fin}")
                with col2:
                    st.write(f"**Chambre:** {selected_room}")
                    st.write(f"**Durée:** {(date_fin - date_debut).days} nuit(s)")
                
                # Confirmation
                if st.button("🎯 Confirmer la réservation", type="primary"):
                    try:
                        new_reservation_id = add_reservation(
                            date_debut.strftime('%Y-%m-%d'), 
                            date_fin.strftime('%Y-%m-%d'), 
                            id_client, 
                            id_chambre
                        )
                        st.success(f"🎉 Réservation créée ! ID: {new_reservation_id}")
                        st.balloons()
                        
                        # Nettoyage
                        if 'available_rooms' in st.session_state:
                            del st.session_state['available_rooms']
                        if 'dates' in st.session_state:
                            del st.session_state['dates']
                            
                    except Exception as e:
                        st.error(f"Erreur: {str(e)}")

# Footer simple
st.markdown("---")
st.markdown("💼 **Système de gestion hôtelière** - Interface simplifiée")