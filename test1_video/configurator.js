const { createApp, ref, onMounted, computed, watch } = Vue

createApp({
    setup() {
        const services = ref([]);
        const cart = ref([]);
        const loading = ref(true);
        const currentStep = ref(1);
        const notifications = ref([]);
        const smartCable = ref(0);
        const clientName = ref('');
        const clientPhone = ref('');
        const sending = ref(false);
        
        // Переменная для хранения выбранного товара для предпросмотра
        const previewItem = ref(null);

        const showToast = (text) => {
            const id = Date.now();
            notifications.value.push({ id, text });
            setTimeout(() => {
                notifications.value = notifications.value.filter(n => n.id !== id);
            }, 3000);
        };

        const validatePhone = (phone) => {
            const clean = phone.replace(/\D/g, '');
            if (clean.length < 11 || clean.length > 15) return false;
            return /^(7|8|375|99)\d{9,12}$/.test(clean);
        };

        const handlePhoneFocus = () => {
            if (!clientPhone.value || clientPhone.value === '') {
                clientPhone.value = '+375';
            }
        };

        const loadData = async () => {
            try {
                const res = await fetch('/api/services');
                const data = await res.json();
                services.value = data.map(s => ({ ...s, tempQty: 1 }));
            } catch (e) {
                console.error(e);
            } finally {
                loading.value = false;
            }
        };

        const camerasCount = computed(() => {
            return cart.value.filter(c => c.name.toLowerCase().includes('камер')).reduce((sum, c) => sum + c.qty, 0);
        });

        const dvrCount = computed(() => {
            return cart.value.filter(c => c.name.toLowerCase().includes('регистр')).reduce((sum, c) => sum + c.qty, 0);
        });

        const mountPriceTotal = computed(() => {
            const srv = services.value.find(s => s.name.toLowerCase().includes('монтаж') && s.name.toLowerCase().includes('камер'));
            return srv ? srv.price * camerasCount.value : 0;
        });

        const dvrWorkPriceTotal = computed(() => {
            const srv = services.value.find(s => (s.name.toLowerCase().includes('настрой') || s.name.toLowerCase().includes('запуск')) && s.name.toLowerCase().includes('регистр'));
            return srv ? srv.price : 0;
        });

        const applyAutoWorks = () => {
            const mountSrv = services.value.find(s => s.name.toLowerCase().includes('монтаж') && s.name.toLowerCase().includes('камер'));
            const dvrSrv = services.value.find(s => (s.name.toLowerCase().includes('настрой') || s.name.toLowerCase().includes('запуск')) && s.name.toLowerCase().includes('регистр'));

            cart.value = cart.value.filter(c => {
                const n = c.name.toLowerCase();
                return !(n.includes('монтаж') && n.includes('камер')) && !( (n.includes('настрой') || n.includes('запуск')) && n.includes('регистр') );
            });

            if (mountSrv && camerasCount.value > 0) {
                cart.value.push({ ...mountSrv, qty: camerasCount.value });
            }
            if (dvrSrv && dvrCount.value > 0) {
                cart.value.push({ ...dvrSrv, qty: 1 });
            }
        };

        watch(currentStep, (newStep) => {
            if (newStep === 3) applyAutoWorks();
        });

        const addToCart = (item) => {
            if (item.tempQty <= 0) return;
            const ex = cart.value.find(c => c.id === item.id);
            if (ex) {
                ex.qty += item.tempQty;
            } else {
                cart.value.push({ ...item, qty: item.tempQty });
            }
            showToast(`Добавлено: ${item.name}`);
        };

        const applySmartCable = () => {
            if (smartCable.value <= 0) return;
            const cableItem = services.value.find(s => s.name.toLowerCase().includes('кабел') || s.name.toLowerCase().includes('utp'));
            const workItem = services.value.find(s => s.name.toLowerCase().includes('прокладка'));
            
            if (cableItem) {
                cart.value = cart.value.filter(c => c.id !== cableItem.id);
                cart.value.push({ ...cableItem, qty: smartCable.value });
            }
            if (workItem) {
                cart.value = cart.value.filter(c => c.id !== workItem.id);
                cart.value.push({ ...workItem, qty: smartCable.value });
            }
            showToast(`Линия ${smartCable.value} м добавлена`);
        };

        const stepServices = computed(() => {
            return services.value.filter(s => {
                const n = s.name.toLowerCase();
                if (currentStep.value === 1) return n.includes('камер');
                if (currentStep.value === 2) return n.includes('регистр') || n.includes('диск');
                return false;
            });
        });

        const stepTitle = computed(() => {
            const titles = { 1: "Выберите камеры", 2: "Хранение данных", 3: "Монтажные работы", 4: "Готовая смета" };
            return titles[currentStep.value];
        });

        const totalSum = computed(() => cart.value.reduce((sum, i) => sum + (i.price * i.qty), 0));
        
        const nextStep = () => currentStep.value++;
        const prevStep = () => currentStep.value--;
        const removeFromCart = (index) => cart.value.splice(index, 1);
        
        const handleOrder = async () => {
            if (!clientName.value.trim()) {
                showToast("Введите ваше имя");
                return;
            }
            if (!validatePhone(clientPhone.value)) {
                showToast("Введите корректный номер телефона");
                return;
            }

            sending.value = true;
            const wishesString = cart.value.map(i => `${i.name} (${i.qty} шт.)`).join(', ');

            const orderData = {
                phone: clientPhone.value.replace(/\D/g, ''),
                total: totalSum.value,
                details: `Заказчик: ${clientName.value}`,
                quiz_data: {
                    object: "Конфигуратор",
                    wishes: wishesString
                }
            };

            try {
                const response = await fetch('/api/orders', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(orderData)
                });

                if (response.ok) {
                    showToast("Заявка успешно отправлена");
                    cart.value = [];
                    clientName.value = '';
                    clientPhone.value = '';
                    currentStep.value = 1;
                } else {
                    showToast("Ошибка при отправке");
                }
            } catch (e) {
                showToast("Ошибка сети");
            } finally {
                sending.value = false;
            }
        };

        onMounted(loadData);

        return { 
            currentStep, stepTitle, stepServices, loading, cart, 
            addToCart, removeFromCart, totalSum, nextStep, prevStep, 
            smartCable, camerasCount, dvrCount, mountPriceTotal, dvrWorkPriceTotal, applySmartCable,
            notifications, handleOrder, clientName, clientPhone, sending, handlePhoneFocus,
            previewItem
        }
    }
}).mount('#app')