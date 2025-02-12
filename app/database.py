from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Crear el objeto db
db = SQLAlchemy()

# Crear la base declarativa
Base = declarative_base()

# Configuración de la base de datos
DATABASE_URL = "sqlite:///reservations.db"  # Cambia esto a tu configuración real
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Inicializar la base de datos al iniciar la aplicación
def init_db(app):
    @app.before_first_request
    def initialize():
        Base.metadata.create_all(bind=engine)


def init_db(app):
    # Configurar la base de datos desde la app Flask
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reservations.db"  # Cambia esto según tu base de datos
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Crear todas las tablas necesarias
