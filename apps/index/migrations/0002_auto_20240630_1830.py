# Generated by Django 5.0.3 on 2024-06-30 22:30

from django.db import migrations


class Migration(migrations.Migration):
    def insert_default_groups(apps, schema_editor):
        Group = apps.get_model('auth', 'Group')
        Group.objects.create(name='administrador')
        Group.objects.create(name='usuario')

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_default_groups),
        migrations.RunSQL(
            '''
            -- Trigger para la creación de un nuevo registro en usuarios_groups
            CREATE OR REPLACE FUNCTION crear_usuario_grupo()
            RETURNS TRIGGER AS $$
            BEGIN
                INSERT INTO auditoria_usuarios (usuario, nombre_usuario, grupo_usuario, fecha)
                VALUES (
                    NEW.usuario_id,
                    (SELECT username FROM usuarios WHERE id = NEW.usuario_id),
                    (SELECT name FROM auth_group WHERE id = NEW.group_id),
                    CURRENT_TIMESTAMP
                );
                RETURN NULL;
            END;
            $$ LANGUAGE plpgsql;

            -- Asociar el trigger a las acciones correspondientes en la tabla usuarios_groups
            CREATE TRIGGER crear_usuario_grupo_trigger AFTER INSERT ON usuarios_groups
            FOR EACH ROW EXECUTE FUNCTION crear_usuario_grupo();

            -- Trigger para la actualización de un registro en usuarios_groups
            CREATE OR REPLACE FUNCTION actualizar_rol_usuario()
            RETURNS TRIGGER AS $$
            DECLARE
                grupo_viejo TEXT;
                grupo_nuevo TEXT;
            BEGIN
                -- Verificar si la actualización implica un cambio en el grupo del usuario
                IF OLD.group_id != NEW.group_id THEN
                    -- Obtener el nombre del grupo viejo y del grupo nuevo
                    SELECT name INTO grupo_viejo FROM auth_group WHERE id = OLD.group_id;
                    SELECT name INTO grupo_nuevo FROM auth_group WHERE id = NEW.group_id;
                    
                    -- Insertar el registro en auditoria_usuarios con el formato deseado
                    INSERT INTO auditoria_usuarios (usuario, nombre_usuario, grupo_usuario, fecha)
                    VALUES (
                        NEW.usuario_id,
                        (SELECT username FROM usuarios WHERE id = NEW.usuario_id),
                        grupo_viejo || ' => ' || grupo_nuevo,
                        CURRENT_TIMESTAMP
                    );
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            -- Asociar el trigger a las acciones correspondientes en la tabla usuarios_groups
            CREATE TRIGGER actualizar_usuario_grupo_trigger AFTER UPDATE ON usuarios_groups
            FOR EACH ROW EXECUTE FUNCTION actualizar_rol_usuario();
            ''' 
            ),
    ]
