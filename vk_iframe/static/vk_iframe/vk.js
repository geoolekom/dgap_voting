VK.init(function() {
    // if (VK.param('viever_type' == 4)) { // TODO check if user is admin
    if (1) {
        VK.addCallback('onAppWidgetPreviewFail', function f(param) {alert(param);});
        VK.callMethod('showGroupSettingsBox', 64);
        VK.callMethod('showAppWidgetPreviewBox', 'compact_list', 'return {"title": "Онлайн-сервисы Сената","rows": [{"title": "Матпомощь","title_url": "https://vk.com/app6216528_-117151095/#aid","button": "Подать заявление","button_url": "https://vk.com/app6216528_-117151095/#aid","text": "Крч все за матпомощью, будете в золоте"}, {"title": "Обращения в Сенат","title_url": "https://vk.com/app6216528_-117151095/#senate","button": "Подать обращение","button_url": "https://vk.com/app6216528_-117151095/#senate", "text": "Прекрасный шанс пообщаться с Кирушей"},{"title": "Бронироание клуба","title_url": "https://vk.com/app6216528_-117151095/#club","button": "Открыть расписание","button_url": "https://vk.com/app6216528_-117151095/#club","text": "Для тех, кто хотел открыть клуб просмтора аниме"},] } ;');
    }
}, function() {
    alert("VK API initialization failed")
}, '5.69');