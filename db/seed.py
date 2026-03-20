from main import SessionLocal, Category, Brand, Service, ServiceSpec, Base, engine

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
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
    db.add_all([b_hik, b_bolid, b_dahua, b_ajax, b_wd, b_sea, b_rex, b_arm])
    db.commit()

    services_to_add = [
        # --- ШАГ 1: КАМЕРЫ ---
        Service(name="IP-камера Hikvision DS-2CD2043G2-I (4Мп)", price_per_unit=245.50, unit_name="шт", category_id=c_video.id, brand_id=b_hik.id),
        Service(name="IP-камера Hikvision DS-2CD2143G2-IS (Купол)", price_per_unit=210.00, unit_name="шт", category_id=c_video.id, brand_id=b_hik.id),
        Service(name="Купольная камера Dahua IPC-HDW2431TP-AS", price_per_unit=198.00, unit_name="шт", category_id=c_video.id, brand_id=b_dahua.id),
        Service(name="Поворотная камера Dahua SD22204UE-GN", price_per_unit=480.00, unit_name="шт", category_id=c_video.id, brand_id=b_dahua.id),

        # --- ШАГ 2: ХРАНЕНИЕ (Регистраторы и HDD) ---
        Service(name="Регистратор Hikvision DS-7604NI-K1 (4 канала)", price_per_unit=320.00, unit_name="шт", category_id=c_video.id, brand_id=b_hik.id),
        Service(name="Регистратор Dahua NVR4108HS-4KS2 (8 каналов)", price_per_unit=410.00, unit_name="шт", category_id=c_video.id, brand_id=b_dahua.id),
        Service(name="Жесткий диск WD Purple 1TB", price_per_unit=185.00, unit_name="шт", category_id=c_video.id, brand_id=b_wd.id),
        Service(name="Жесткий диск WD Purple 2TB", price_per_unit=240.00, unit_name="шт", category_id=c_video.id, brand_id=b_wd.id),
        Service(name="Жесткий диск Seagate SkyHawk 4TB", price_per_unit=380.00, unit_name="шт", category_id=c_video.id, brand_id=b_sea.id),

        # --- ШАГ 3: МОНТАЖ И КАБЕЛЬ ---
        Service(name="Кабель витая пара UTP Cat5e Cu (Медь)", price_per_unit=1.20, unit_name="м", category_id=c_video.id, brand_id=b_rex.id),
        Service(name="Кабель КВК-П-2 2х0.75 (Уличный)", price_per_unit=1.50, unit_name="м", category_id=c_video.id, brand_id=b_rex.id),
        Service(name="Монтаж и настройка камеры", price_per_unit=85.00, unit_name="услуга", category_id=c_video.id, brand_id=b_arm.id),
        Service(name="Установка и запуск видеорегистратора", price_per_unit=120.00, unit_name="услуга", category_id=c_video.id, brand_id=b_arm.id),
        Service(name="Прокладка кабеля (в гофре/коробе)", price_per_unit=2.50, unit_name="м", category_id=c_video.id, brand_id=b_arm.id),
        Service(name="Разъем BNC/RJ45 + расходные материалы", price_per_unit=5.00, unit_name="комплект", category_id=c_video.id, brand_id=b_rex.id),

        # --- ПОЖАРКА ---
        Service(name="Датчик дыма ИП 212-141", price_per_unit=15.20, unit_name="шт", category_id=c_fire.id, brand_id=b_bolid.id),
        Service(name="Пульт С2000-М", price_per_unit=280.00, unit_name="шт", category_id=c_fire.id, brand_id=b_bolid.id),

        # --- ОХРАНКА ---
        Service(name="Датчик движения Ajax MotionProtect", price_per_unit=145.00, unit_name="шт", category_id=c_guard.id, brand_id=b_ajax.id),
        Service(name="Централь Ajax Hub 2 (4G)", price_per_unit=450.00, unit_name="шт", category_id=c_guard.id, brand_id=b_ajax.id),
        Service(name="Уличная сирена Ajax StreetSiren", price_per_unit=210.00, unit_name="шт", category_id=c_guard.id, brand_id=b_ajax.id)
    ]
    
    db.add_all(services_to_add)
    db.commit()

    # Добавим спецификации для красоты
    specs = [
        ServiceSpec(service_id=services_to_add[0].id, spec_name="Разрешение", spec_value="4 Мп"),
        ServiceSpec(service_id=services_to_add[4].id, spec_name="Формат", spec_value="H.265+"),
        ServiceSpec(service_id=services_to_add[6].id, spec_name="Назначение", spec_value="Для систем видеонаблюдения"),
        ServiceSpec(service_id=services_to_add[9].id, spec_name="Материал", spec_value="Чистая медь")
    ]
    
    db.add_all(specs)
    db.commit()
    
    print(f"✅ База данных успешно наполнена! Добавлено {len(services_to_add)} позиций.")
    db.close()

if __name__ == "__main__":
    seed_data()