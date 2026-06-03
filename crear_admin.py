# crear_admin.py

from app import create_app, db
from app.models.usuario import Usuario

app = create_app()

with app.app_context():
    admin = Usuario.query.filter_by(email='admin@admin.com').first()
    
    if admin:
        if admin.rol != 'Superadmin':
            admin.rol = 'Superadmin'
            db.session.commit()
            print("=" * 40)
            print("✅ Usuario actualizado a Superadmin")
            print(f"📧 Email: {admin.email}")
            print("=" * 40)
        else:
            print("=" * 40)
            print("⚠️ Usuario ya existe como Superadmin")
            print(f"📧 Email: {admin.email}")
            print("=" * 40)
    else:
        admin = Usuario(
            nombre='Admin',
            email='admin@admin.com',
            cedula='12345678',
            rol='Superadmin',
            departamento='Operaciones',
            telefono='00000000',
            activo=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        
        print("=" * 40)
        print("✅ Superadmin creado exitosamente!")
        print(f"📧 Email: admin@admin.com")
        print(f"🔑 Contraseña: admin123")
        print("=" * 40)