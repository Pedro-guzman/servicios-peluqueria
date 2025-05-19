import os
import subprocess
import sys

def main():
    # Navega al directorio del proyecto
    os.chdir('/Users/pedroguzmancarlos/Desktop/proyecto_dejango')

    # Activa el entorno virtual
    activate_env = os.path.expanduser("venv/bin/activate_this.py")
    with open(activate_env) as f:
        exec(f.read(), {'__file__': activate_env})

    # Aplica las migraciones
    subprocess.check_call([sys.executable, 'manage.py', 'migrate'])

    # Corre el servidor Django
    subprocess.check_call([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'])

if __name__ == '__main__':
    main()

