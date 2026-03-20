from main import SessionLocal, Category, Brand, Service, ServiceSpec, User, Base, engine

def seed_data():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    admin_user = User(username="admin", hashed_password="123", role="admin")
    manager_user = User(username="manager", hashed_password="456", role="manager")
    db.add_all([admin_user, manager_user])
    db.commit()

    c_video = Category(name="Видеонаблюдение")
    c_fire = Category(name="Пожарная безопасность")
    c_guard = Category(name="Охранная сигнализация")
    db.add_all([c_video, c_fire, c_guard])
    db.commit()

    b_hik = Brand(name="Hikvision")
    b_bolid = Brand(name="Bolid")
    b_dahua = Brand(name="Dahua")
    b_ajax = Brand(name="Ajax")
    b_wd = Brand(name="Western Digital")
    b_sea = Brand(name="Seagate")
    b_rex = Brand(name="Rexant")
    b_arm = Brand(name="Армстрим")
    b_lite = Brand(name="HiWatch")
    db.add_all([b_hik, b_bolid, b_dahua, b_ajax, b_wd, b_sea, b_rex, b_arm, b_lite])
    db.commit()

    services_to_add = [
        Service(name="IP-камера Hikvision DS-2CD2043G2-I (4Мп)", price_per_unit=245.50, unit_name="шт", category_id=c_video.id, brand_id=b_hik.id, image="hik_cyl.jpg", difficulty_factor=1.2),
        Service(name="IP-камера Hikvision DS-2CD2143G2-IS (Купол)", price_per_unit=210.00, unit_name="шт", category_id=c_video.id, brand_id=b_hik.id, image="hik_dome.jpg", difficulty_factor=1.1),
        Service(name="Купольная камера Dahua IPC-HDW2431TP-AS", price_per_unit=198.00, unit_name="шт", category_id=c_video.id, brand_id=b_dahua.id, image="dahua_dome.jpg", difficulty_factor=1.1),
        Service(name="Поворотная камера Dahua SD22204UE-GN", price_per_unit=480.00, unit_name="шт", category_id=c_video.id, brand_id=b_dahua.id, image="dahua_ptz.jpg", difficulty_factor=1.5),
        Service(name="Бюджетная камера HiWatch IPC-D022-G2", price_per_unit=145.00, unit_name="шт", category_id=c_video.id, brand_id=b_lite.id, image="hiwatch_d022.jpg", difficulty_factor=1.0),

        Service(name="Регистратор Hikvision DS-7604NI-K1 (4 канала)", price_per_unit=320.00, unit_name="шт", category_id=c_video.id, brand_id=b_hik.id, image="hik_nvr4.jpg", difficulty_factor=1.3),
        Service(name="Регистратор Dahua NVR4108HS-4KS2 (8 каналов)", price_per_unit=410.00, unit_name="шт", category_id=c_video.id, brand_id=b_dahua.id, image="dahua_nvr8.jpg", difficulty_factor=1.4),
        Service(name="Жесткий диск WD Purple 1TB", price_per_unit=185.00, unit_name="шт", category_id=c_video.id, brand_id=b_wd.id, image="wd_1tb.jpg", difficulty_factor=1.0),
        Service(name="Жесткий диск WD Purple 2TB", price_per_unit=240.00, unit_name="шт", category_id=c_video.id, brand_id=b_wd.id, image="wd_2tb.jpg", difficulty_factor=1.0),
        Service(name="Жесткий диск Seagate SkyHawk 4TB", price_per_unit=380.00, unit_name="шт", category_id=c_video.id, brand_id=b_sea.id, image="sea_4tb.jpg", difficulty_factor=1.0),

        Service(name="Кабель витая пара UTP Cat5e Cu (Медь)", price_per_unit=1.20, unit_name="м", category_id=c_video.id, brand_id=b_rex.id, image="utp_cable.jpg", difficulty_factor=1.0),
        Service(name="Кабель КВК-П-2 2х0.75 (Уличный)", price_per_unit=1.50, unit_name="м", category_id=c_video.id, brand_id=b_rex.id, image="kvk_cable.jpg", difficulty_factor=1.1),
        Service(name="Монтаж и настройка камеры", price_per_unit=85.00, unit_name="услуга", category_id=c_video.id, brand_id=b_arm.id, image="work_cam.jpg", difficulty_factor=1.2),
        Service(name="Установка и запуск видеорегистратора", price_per_unit=120.00, unit_name="услуга", category_id=c_video.id, brand_id=b_arm.id, image="work_nvr.jpg", difficulty_factor=1.3),
        Service(name="Прокладка кабеля (в гофре/коробе)", price_per_unit=2.50, unit_name="м", category_id=c_video.id, brand_id=b_arm.id, image="work_cable.jpg", difficulty_factor=1.4),
        Service(name="Разъем BNC/RJ45 + расходные материалы", price_per_unit=5.00, unit_name="комплект", category_id=c_video.id, brand_id=b_rex.id, image="connectors.jpg", difficulty_factor=1.0),

        Service(name="Датчик дыма ИП 212-141", price_per_unit=15.20, unit_name="шт", category_id=c_fire.id, brand_id=b_bolid.id, image="fire_smoke.jpg", difficulty_factor=1.0),
        Service(name="Пульт С2000-М", price_per_unit=280.00, unit_name="шт", category_id=c_fire.id, brand_id=b_bolid.id, image="bolid_c2000.jpg", difficulty_factor=1.2),
        Service(name="Тепловой извещатель ИП 101-1А", price_per_unit=12.50, unit_name="шт", category_id=c_fire.id, brand_id=b_bolid.id, image="fire_heat.jpg", difficulty_factor=1.0),
        Service(name="Блок питания С2000-АСПТ", price_per_unit=310.00, unit_name="шт", category_id=c_fire.id, brand_id=b_bolid.id, image="bolid_aspt.jpg", difficulty_factor=1.3),

        Service(name="Датчик движения Ajax MotionProtect", price_per_unit=145.00, unit_name="шт", category_id=c_guard.id, brand_id=b_ajax.id, image="ajax_motion.jpg", difficulty_factor=1.0),
        Service(name="Централь Ajax Hub 2 (4G)", price_per_unit=450.00, unit_name="шт", category_id=c_guard.id, brand_id=b_ajax.id, image="ajax_hub.jpg", difficulty_factor=1.2),
        Service(name="Уличная сирена Ajax StreetSiren", price_per_unit=210.00, unit_name="шт", category_id=c_guard.id, brand_id=b_ajax.id, image="ajax_siren.jpg", difficulty_factor=1.1),
        Service(name="Датчик открытия DoorProtect", price_per_unit=95.00, unit_name="шт", category_id=c_guard.id, brand_id=b_ajax.id, image="ajax_door.jpg", difficulty_factor=1.0)
    ]
    
    db.add_all(services_to_add)
    db.commit()

    specs = [
        ServiceSpec(service_id=services_to_add[0].id, spec_name="Разрешение", spec_value="4 Мп"),
        ServiceSpec(service_id=services_to_add[0].id, spec_name="ИК-подсветка", spec_value="30 м"),
        ServiceSpec(service_id=services_to_add[3].id, spec_name="Оптический зум", spec_value="4x"),
        ServiceSpec(service_id=services_to_add[5].id, spec_name="Макс. разрешение", spec_value="8 Мп (4K)"),
        ServiceSpec(service_id=services_to_add[5].id, spec_name="Входящий поток", spec_value="40 Мбит/с"),
        ServiceSpec(service_id=services_to_add[7].id, spec_name="Кэш-память", spec_value="64 Мб"),
        ServiceSpec(service_id=services_to_add[10].id, spec_name="Материал проводника", spec_value="Медь (Cu)"),
        ServiceSpec(service_id=services_to_add[21].id, spec_name="Дальность связи", spec_value="до 2000 м"),
        ServiceSpec(service_id=services_to_add[21].id, spec_name="Каналы связи", spec_value="Ethernet, 2x SIM (2G/3G/4G)")
    ]
    
    db.add_all(specs)
    db.commit()
    
    print(f"✅ База данных пересоздана и наполнена! Добавлено {len(services_to_add)} товаров и 2 пользователя.")
    db.close()

if __name__ == "__main__":
    seed_data()