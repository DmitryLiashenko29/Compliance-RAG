# Эталонные вопросы для КП2

Compliance RAG · Янаков Роман · Агент Критик

Подготовлено 10 ноября 2026 года. 30 вопросов и 12 сценариев отдельной проверки Критика. Ответы составлены по зафиксированным исходным текстам. Командная проверка разметки и прогоны моделей ещё предстоят.

## Границы набора

Выбраны Reddit и YouTube из Open Terms Archive. Это предложенный учебный корпус для КП2; согласование выбора с участником, готовящим документы, ещё требуется. Вопросы относятся к указанным редакциям и выделенным диапазонам строк. Английские источники сопровождаются русскими вопросами и эталонными ответами.

Reddit представлен редакциями 2025–2026 годов, YouTube — 2023 года. Выбор расширяет диапазон 2022–2024 из исходной презентации. При сохранении этого диапазона как обязательного ограничения вопросы Reddit нужно переразметить по другим источникам.

Дата коммита означает время записи архива. По ней нельзя автоматически устанавливать дату действия правил. Y1 и Y2 записаны в один день, поэтому версию необходимо идентифицировать полным SHA, а не только датой.

| ID | Документ | Запись архива, UTC | Источник |
|---|---|---|---|
| R1 | Reddit/Community Guidelines.md | 2025-10-23T12:38:16Z | [aadf0e1](https://github.com/OpenTermsArchive/pga-versions/blob/aadf0e11ed449a10f83b93e7c7164d5c812e8208/Reddit/Community%20Guidelines.md) |
| R2 | Reddit/Community Guidelines.md | 2026-11-06T00:52:52Z | [735fc4b](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md) |
| Y1 | YouTube/Community Guidelines.md | 2023-06-02T06:35:04Z | [d6ddd00](https://github.com/OpenTermsArchive/pga-versions/blob/d6ddd0003c305ba46d51eada405888556cccc54b/YouTube/Community%20Guidelines.md) |
| Y2 | YouTube/Community Guidelines.md | 2023-06-02T18:35:13Z | [30e6af9](https://github.com/OpenTermsArchive/pga-versions/blob/30e6af989d9b8656fddad0dbb4086b2efa3e3a0c/YouTube/Community%20Guidelines.md) |

Корпус задаётся объединением диапазонов в разделе «Фрагменты источников». Тексты страниц, на которые ссылаются сами правила, не входят в корпус. Добавление других разделов или документов требует повторной проверки меток «нет ответа».

## Состав

| Тип | Количество |
|---|---|
| Прямой вопрос | 8 |
| Несколько фактов или условий | 6 |
| Изменение или уточнение версии | 6 |
| Без изменения правила | 2 |
| Нет ответа в выбранном корпусе | 5 |
| Нужно уточнение | 3 |

Вопросы одной темы связаны между собой. 30 формулировок не означают 30 независимых правил. Изменения версий включают уточнения и сужение области применения. Неразрешимые противоречия для одной даты и одной области применения отдельно не подтверждены.

## Карточки вопросов

### Q01 · Прямой вопрос

**Вопрос** — Можно ли использовать Reddit без настоящего имени по редакции R2?

**Эталонный ответ** — Да. Использование настоящего имени не обязательно, но запрещено вводить других в заблуждение относительно личности или принадлежности к организации.

**Критерий проверки** — Не превращать разрешение псевдонима в разрешение обманного представления.

**Доказательства** — [R2_rule5 · Rules / Rule 5](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L31-L33), [R2_impersonation · Разъяснение Rule 5 / impersonation](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L459-L497).

### Q02 · Прямой вопрос

**Вопрос** — Считается ли спамом только автоматическая массовая активность по редакции R2?

**Эталонный ответ** — Нет. Определение охватывает как автоматические, так и ручные повторяющиеся или нежелательные действия, которые негативно влияют на пользователей, сообщества или Reddit.

**Критерий проверки** — Сохранить условие негативного влияния и различие между ручным и автоматическим действием.

**Доказательства** — [R2_spam · Разъяснение Rule 2 / spam](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L223-L260).

### Q03 · Прямой вопрос

**Вопрос** — К кому обратиться, если непонятно, считается ли публикация спамом в конкретном сообществе Reddit по R2?

**Эталонный ответ** — Проверить дополнительные правила сообщества и обратиться за разъяснением к его модераторам.

**Критерий проверки** — Указать оба действия.

**Доказательства** — [R2_spam · Разъяснение Rule 2 / spam](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L223-L260).

### Q04 · Прямой вопрос

**Вопрос** — Разрешает ли R2 только просматривать сообщество Reddit после блокировки в нём, без участия?

**Эталонный ответ** — Да. Просмотр без взаимодействия приведён как пример поведения, не нарушающего это правило.

**Критерий проверки** — Не расширять ответ на публикации и обход блокировки.

**Доказательства** — [R2_disruption · Разъяснение Rule 2 / disruptive behaviors](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L264-L304).

### Q05 · Прямой вопрос

**Вопрос** — Разрешает ли R2 публиковать личные данные человека только потому, что они уже доступны на другом сайте?

**Эталонный ответ** — Нет автоматического разрешения. Доступность в другом месте не делает публикацию допустимой, если она создаёт риск для безопасности человека.

**Критерий проверки** — Не смешивать личные данные с ограниченными исключениями для официальных профессиональных контактов.

**Доказательства** — [R2_privacy · Разъяснение Rule 3 / personal information](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L308-L350).

### Q06 · Прямой вопрос

**Вопрос** — Что требует Rule 6 в R2 от маркировки контента и сообществ Reddit?

**Эталонный ответ** — Нужно корректно маркировать контент и сообщества, особенно содержащие графические, сексуально откровенные или оскорбительные материалы.

**Критерий проверки** — Не выдумывать технический механизм или список обязательных тегов сверх источника.

**Доказательства** — [R2_rule6 · Rules / Rule 6](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L35-L37).

### Q07 · Прямой вопрос

**Вопрос** — Какие меры к аккаунтам перечислены в Enforcement редакции R2?

**Эталонный ответ** — Временная или постоянная приостановка аккаунта, снятие привилегий либо добавление ограничений. Перечень мер в документе открытый.

**Критерий проверки** — Не утверждать, что это исчерпывающий список или обязательная последовательность.

**Доказательства** — [R2_enforcement · Enforcement](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L47-L57).

### Q08 · Прямой вопрос

**Вопрос** — Можно ли по R2 создавать аккаунты Reddit автоматизированными или агентными средствами?

**Эталонный ответ** — Такое создание аккаунтов прямо включено в примеры нарушений разъяснения Rule 8.

**Критерий проверки** — Сослаться на расширенное разъяснение, а не только краткий Rule 8.

**Доказательства** — [R2_site · Разъяснение Rule 8 / normal use and API](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L554-L574).

### Q09 · Несколько фактов или условий

**Вопрос** — Разрешены ли по R2 псевдоним и фан-аккаунт знаменитости, и где проходит граница допустимого?

**Эталонный ответ** — Псевдоним допустим. Фан-аккаунт допустим, если не присваивает личность знаменитости при общении. Обманное представление личности или связи с организацией запрещено; для фанатских и пародийных аккаунтов рекомендуется ясно обозначать назначение.

**Критерий проверки** — Не превращать рекомендацию раскрыть назначение аккаунта в безусловную формальную обязанность.

**Доказательства** — [R2_rule5 · Rules / Rule 5](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L31-L33), [R2_impersonation · Разъяснение Rule 5 / impersonation](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L459-L497).

### Q10 · Несколько фактов или условий

**Вопрос** — Как по R2 различаются спам и манипуляция голосами?

**Эталонный ответ** — Спам — повторяющиеся или нежелательные действия с негативным влиянием, в том числе массовые публикации. Манипуляция голосами включает искусственное изменение голосования через несколько аккаунтов, сервисы, автоматизацию или координацию группы. Оба поведения запрещены.

**Критерий проверки** — Нужны подтверждения обоих понятий.

**Доказательства** — [R2_spam · Разъяснение Rule 2 / spam](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L223-L260), [R2_disruption · Разъяснение Rule 2 / disruptive behaviors](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L264-L304).

### Q11 · Несколько фактов или условий

**Вопрос** — Можно ли по R2 публиковать официальный рабочий контакт публичного лица и одновременно его домашний адрес?

**Эталонный ответ** — Для официальных публичных профессиональных каналов связи предусмотрены ограниченные исключения. Они не распространяются на частную информацию, включая домашний адрес, и не разрешают травлю.

**Критерий проверки** — Разделить официальный контакт и частные сведения.

**Доказательства** — [R2_rule3 · Rules / Rule 3](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L23-L25), [R2_privacy · Разъяснение Rule 3 / personal information](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L308-L350).

### Q12 · Несколько фактов или условий

**Вопрос** — Разрешает ли R2 резко критиковать публичное лицо и преследовать его семью в ходе такой критики?

**Эталонный ответ** — Резкая критика публичной роли допустима. Кампании преследования семьи, угроза личной безопасности и подстрекательство к серьёзному вреду исключением не покрываются.

**Критерий проверки** — Проверить обе части вопроса по разным абзацам одного разъяснения.

**Доказательства** — [R2_harassment · Разъяснение Rule 1 / harassment](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L61-L102).

### Q13 · Несколько фактов или условий

**Вопрос** — Разрешает ли R2 создать второй аккаунт для обхода блокировки сообщества и просто читать это сообщество без участия?

**Эталонный ответ** — Использовать другой аккаунт для обхода блокировки запрещено. Сам по себе просмотр контента заблокированного сообщества без взаимодействия приведён как допустимый пример.

**Критерий проверки** — Не объединять два разных действия в одно общее разрешение или запрет.

**Доказательства** — [R2_disruption · Разъяснение Rule 2 / disruptive behaviors](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L264-L304).

### Q14 · Несколько фактов или условий

**Вопрос** — Какие ограничения R2 описывает для приложения, которое показывает удалённый пользователем контент и рассылает незапрошенные сообщения автоматически?

**Эталонный ответ** — Продолжение использования или показа удалённого контента и автоматизация незапрошенных обращений указаны как нарушения. Приложения также должны регистрироваться и соблюдать перечисленные в источнике правила для разработчиков.

**Критерий проверки** — Покрыть оба действия. Не выдумывать срок удаления копий.

**Доказательства** — [R2_site · Разъяснение Rule 8 / normal use and API](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L554-L574).

### Q15 · Изменение или уточнение версии

**Вопрос** — Какие выборы прямо перечислены в Election integrity редакции Y1 и что изменилось в Y2?

**Эталонный ответ** — Y1 перечисляет любые прошедшие президентские выборы США, федеральные выборы Германии 2021 года и президентские выборы Бразилии 2014, 2018 и 2022 годов. В Y2 элемент про США удалён, элементы про Германию и Бразилию сохранены.

**Критерий проверки** — Нужны обе версии. Изменение этого пункта не доказывает отмену всех правил о выборах.

**Доказательства** — [Y1_elections · Elections misinformation policies](https://github.com/OpenTermsArchive/pga-versions/blob/d6ddd0003c305ba46d51eada405888556cccc54b/YouTube/Community%20Guidelines.md#L1670-L1745), [Y2_elections · Elections misinformation policies](https://github.com/OpenTermsArchive/pga-versions/blob/30e6af989d9b8656fddad0dbb4086b2efa3e3a0c/YouTube/Community%20Guidelines.md#L1670-L1741).

### Q16 · Изменение или уточнение версии

**Вопрос** — Сохранился ли в Y2 по сравнению с Y1 пример о ложных заявлениях относительно результата президентских выборов США 2020 года?

**Эталонный ответ** — Нет. Пример, прямо относящийся к ложному утверждению о сфальсифицированных или украденных выборах США 2020 года, присутствует в Y1 и удалён из Y2.

**Критерий проверки** — Не отвечать по старой версии и не обобщать на весь политический контент.

**Доказательства** — [Y1_elections · Elections misinformation policies](https://github.com/OpenTermsArchive/pga-versions/blob/d6ddd0003c305ba46d51eada405888556cccc54b/YouTube/Community%20Guidelines.md#L1670-L1745), [Y2_elections · Elections misinformation policies](https://github.com/OpenTermsArchive/pga-versions/blob/30e6af989d9b8656fddad0dbb4086b2efa3e3a0c/YouTube/Community%20Guidelines.md#L1670-L1741).

### Q17 · Изменение или уточнение версии

**Вопрос** — Убрали ли в Y2 весь пункт Election integrity вместе с упоминанием США?

**Эталонный ответ** — Нет. В Y2 сохранились правило и перечисление выборов Германии и Бразилии; удалены элемент списка про США и связанные примеры.

**Критерий проверки** — Отклонить ложную предпосылку вопроса.

**Доказательства** — [Y1_elections · Elections misinformation policies](https://github.com/OpenTermsArchive/pga-versions/blob/d6ddd0003c305ba46d51eada405888556cccc54b/YouTube/Community%20Guidelines.md#L1670-L1745), [Y2_elections · Elections misinformation policies](https://github.com/OpenTermsArchive/pga-versions/blob/30e6af989d9b8656fddad0dbb4086b2efa3e3a0c/YouTube/Community%20Guidelines.md#L1670-L1741).

### Q18 · Изменение или уточнение версии

**Вопрос** — Как изменилось описание приложений и автоматизации в разъяснении Rule 8 между R1 и R2?

**Эталонный ответ** — R1 кратко запрещает нарушение работы сайта, вредоносный код, блокирование рекламных заголовков и программы, нарушающие API-правила. R2 раскрывает область применения для приложений, ботов и AI-агентов и добавляет явные пункты о регистрации, удалённом контенте, незапрошенной автоматической рассылке и автоматизированном создании аккаунтов.

**Критерий проверки** — Отсутствие явного пункта в R1 не означает, что соответствующее действие тогда было разрешено.

**Доказательства** — [R1_site · Разъяснение Rule 8 / normal use and API](https://github.com/OpenTermsArchive/pga-versions/blob/aadf0e11ed449a10f83b93e7c7164d5c812e8208/Reddit/Community%20Guidelines.md#L374-L374), [R2_site · Разъяснение Rule 8 / normal use and API](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L554-L574).

### Q19 · Изменение или уточнение версии

**Вопрос** — Как изменились пояснения к исключениям для публичных лиц в правилах приватности между R1 и R2?

**Эталонный ответ** — В обеих редакциях есть ограниченное исключение для профессиональных контактов публичных лиц и запрет травли. R2 подробнее ограничивает исключение официальными публичными рабочими каналами и явно исключает частные сведения о самом лице и его семье.

**Критерий проверки** — Описать уточнение и общий смысл. Не объявлять противоположными совместимые формулировки.

**Доказательства** — [R1_privacy · Разъяснение Rule 3 / personal information](https://github.com/OpenTermsArchive/pga-versions/blob/aadf0e11ed449a10f83b93e7c7164d5c812e8208/Reddit/Community%20Guidelines.md#L200-L206), [R2_privacy · Разъяснение Rule 3 / personal information](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L308-L350).

### Q20 · Изменение или уточнение версии

**Вопрос** — Какие дополнительные разъяснения о критике публичных лиц появились в R2 по сравнению с R1?

**Эталонный ответ** — R1 отделяет несогласие и отрицательные оценки от преследования. R2 подробнее описывает допустимую критику идей, организаций и публичных лиц и отдельно ограничивает кампании против семьи, личной безопасности и подстрекательство к серьёзному вреду.

**Критерий проверки** — Назвать добавленные разъяснения без утверждения, что вся критика раньше запрещалась.

**Доказательства** — [R1_harassment · Разъяснение Rule 1 / harassment](https://github.com/OpenTermsArchive/pga-versions/blob/aadf0e11ed449a10f83b93e7c7164d5c812e8208/Reddit/Community%20Guidelines.md#L61-L67), [R2_harassment · Разъяснение Rule 1 / harassment](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L61-L102).

### Q21 · Без изменения правила

**Вопрос** — Изменилось ли между R1 и R2 правило об обязательности настоящего имени в Rule 5?

**Эталонный ответ** — Нет. В обеих редакциях настоящее имя не обязательно, а намеренное введение в заблуждение и обманное представление другого лица запрещены.

**Критерий проверки** — Две версии сами по себе не образуют конфликт.

**Доказательства** — [R1_rule5 · Rules / Rule 5](https://github.com/OpenTermsArchive/pga-versions/blob/aadf0e11ed449a10f83b93e7c7164d5c812e8208/Reddit/Community%20Guidelines.md#L31-L33), [R2_rule5 · Rules / Rule 5](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L31-L33).

### Q22 · Без изменения правила

**Вопрос** — Изменилась ли формулировка Rule 6 о маркировке контента между R1 и R2?

**Эталонный ответ** — Нет. Проверяемый текст Rule 6 в этих двух редакциях совпадает.

**Критерий проверки** — Зафиксировать отсутствие изменения именно этого пункта.

**Доказательства** — [R1_rule6 · Rules / Rule 6](https://github.com/OpenTermsArchive/pga-versions/blob/aadf0e11ed449a10f83b93e7c7164d5c812e8208/Reddit/Community%20Guidelines.md#L35-L37), [R2_rule6 · Rules / Rule 6](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L35-L37).

### Q23 · Нет ответа в выбранном корпусе

**Вопрос** — В течение скольких часов Reddit обязан рассмотреть жалобу на спам по материалам R2?

**Эталонный ответ** — В выбранных материалах R2 описан способ пожаловаться, но конкретный срок рассмотрения в часах отсутствует. Данных для такого срока недостаточно.

**Критерий проверки** — Сослаться на границы выбранного корпуса. Не выдавать предположение за срок.

**Смежные фрагменты** — [R2_spam](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L223-L260), [R2_enforcement](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L47-L57). Они описывают тему, но не подтверждают запрошенное число или срок. Проверены все выбранные диапазоны соответствующего снимка.

### Q24 · Нет ответа в выбранном корпусе

**Вопрос** — Через сколько часов приложение обязано удалить локальную копию контента после его удаления пользователем по R2?

**Эталонный ответ** — R2 запрещает продолжать использование или показ удалённого контента, но точное число часов в выбранных материалах не указано.

**Критерий проверки** — Отличить наличие требования от наличия числового срока.

**Смежные фрагменты** — [R2_site](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L554-L574). Они описывают тему, но не подтверждают запрошенное число или срок. Проверены все выбранные диапазоны соответствующего снимка.

### Q25 · Нет ответа в выбранном корпусе

**Вопрос** — Каков фиксированный денежный штраф Reddit за нарушение Rule 5 в R2?

**Эталонный ответ** — В выбранных материалах не установлен фиксированный денежный штраф за такое нарушение. Данных для суммы недостаточно.

**Критерий проверки** — Не выводить сумму из списка мер к аккаунтам.

**Смежные фрагменты** — [R2_rule5](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L31-L33), [R2_enforcement](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L47-L57). Они описывают тему, но не подтверждают запрошенное число или срок. Проверены все выбранные диапазоны соответствующего снимка.

### Q26 · Нет ответа в выбранном корпусе

**Вопрос** — Какое максимальное число часов YouTube отводит на рассмотрение жалобы по Election integrity в Y2?

**Эталонный ответ** — В выбранном разделе Y2 есть указание сообщать о нарушениях, но максимальный срок рассмотрения жалобы в часах отсутствует.

**Критерий проверки** — Не переходить к внешним страницам и не приписывать срок выбранному разделу.

**Смежные фрагменты** — [Y2_elections](https://github.com/OpenTermsArchive/pga-versions/blob/30e6af989d9b8656fddad0dbb4086b2efa3e3a0c/YouTube/Community%20Guidelines.md#L1670-L1741). Они описывают тему, но не подтверждают запрошенное число или срок. Проверены все выбранные диапазоны соответствующего снимка.

### Q27 · Нет ответа в выбранном корпусе

**Вопрос** — Какой размер компенсации положен пользователю за раскрытие его личной информации по выбранным материалам R2?

**Эталонный ответ** — Выбранные материалы запрещают раскрытие личных данных, но не устанавливают размер компенсации. Данных для расчёта или суммы недостаточно.

**Критерий проверки** — Не подменять ответ внешними правовыми знаниями.

**Смежные фрагменты** — [R2_privacy](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L308-L350). Они описывают тему, но не подтверждают запрошенное число или срок. Проверены все выбранные диапазоны соответствующего снимка.

### Q28 · Нужно уточнение

**Вопрос** — Удалено ли упоминание президентских выборов США из Election integrity в версии YouTube от 2 июня 2023 года?

**Эталонный ответ** — Нужно уточнить редакцию или время снимка. В наборе есть два коммита за 2 июня 2023 года: Y1 содержит элемент про США, Y2 его уже не содержит.

**Критерий проверки** — Запросить SHA/время либо явно описать оба снимка; не выбирать молча.

**Доказательства** — [Y1_elections · Elections misinformation policies](https://github.com/OpenTermsArchive/pga-versions/blob/d6ddd0003c305ba46d51eada405888556cccc54b/YouTube/Community%20Guidelines.md#L1670-L1745), [Y2_elections · Elections misinformation policies](https://github.com/OpenTermsArchive/pga-versions/blob/30e6af989d9b8656fddad0dbb4086b2efa3e3a0c/YouTube/Community%20Guidelines.md#L1670-L1741).

### Q29 · Нужно уточнение

**Вопрос** — Можно ли это публиковать?

**Эталонный ответ** — Недостаточно условий вопроса. Нужно уточнить, какой материал, на какой платформе и по какой редакции требуется проверить.

**Критерий проверки** — Уточнить запрос до содержательного вердикта.

**Ожидание** — уточнить недостающие условия. Источник для прямого содержательного ответа не выбран.

### Q30 · Нужно уточнение

**Вопрос** — Какие правила действуют сейчас?

**Эталонный ответ** — Нужно уточнить платформу и тему. Набор содержит исторические снимки и не подтверждает полноту действующих сегодня правил; следует указать эту границу.

**Критерий проверки** — Не объявлять наиболее свежую загруженную редакцию действующей сегодня.

**Ожидание** — уточнить недостающие условия. Источник для прямого содержательного ответа не выбран.

## Сценарии отдельной проверки Критика

Для этих сценариев выдача Поиска фиксируется вручную. ID фрагментов указывают на тексты в реестре ниже. Ожидаемые действия относятся к конкретной выдаче и флагу завершения поиска.

| Сценарий | Вопрос | Переданные фрагменты | Поиск исчерпан | Действие | Объяснение |
|---|---|---|---|---|---|
| C01 | Q01 | R2_rule5, R2_impersonation | Нет | pass | Доказательств для разрешения псевдонима и ограничения обмана достаточно. |
| C02 | Q10 | R2_spam | Нет | search_more | Нужны фрагменты о манипуляции голосами из R2. |
| C03 | Q15 | Y1_elections, Y2_elections | Нет | pass | Можно сопоставить обе редакции и точно описать удаление элемента про США. |
| C04 | Q15 | Y2_elections | Нет | search_more | Для ответа об изменении нужен соответствующий раздел Y1. |
| C05 | Q21 | R1_rule5, R2_rule5 | Нет | pass | Текст проверяемого правила совпадает. |
| C06 | Q08 | R1_site | Нет | search_more | Вопрос относится к R2, а передано разъяснение R1. |
| C07 | Q23 | R2_spam | Нет | search_more | Срок рассмотрения не найден; запросить сведения именно о сроке. |
| C08 | Q23 | R2_spam, R2_enforcement | Да | insufficient | Лимит поиска исчерпан; переданные материалы не подтверждают срок в часах. |
| C09 | Q28 | Y1_elections, Y2_elections | Нет | clarify | Две редакции имеют одну календарную дату; нужен SHA или время снимка. Допустим условный ответ по обеим версиям. |
| C10 | Q11 | R2_rule3 | Нет | search_more | Краткий Rule 3 не раскрывает условия исключения для публичных профессиональных контактов. |
| C11 | Q15 | R2_disruption, R2_rule5 | Нет | search_more | Переданы сведения о другой платформе и другой теме. |
| C12 | Q19 | R1_privacy, R2_privacy | Нет | pass | Исключение есть в обеих версиях, в R2 добавлены ограничения. Не помечать всё как неразрешимое противоречие. |

Действия — `pass` означает передачу доказательств Агенту Ответа, `search_more` запрос недостающих сведений, `insufficient` недостаточность после исчерпания поиска, `clarify` уточнение пользователя. Метки предложены для согласования с командой.

## Фрагменты источников

Каждый фрагмент — точный непрерывный диапазон строк исходного Markdown в зафиксированном коммите. ID здесь — идентификаторы контрольных фрагментов. После чанкинга нужно сохранить их соответствие новым chunk_id. Заголовки разъяснений без собственного номера привязаны к соответствующему Rule; новые номера пунктов не придуманы.

| ID | Раздел | Строки исходника | Ссылка |
|---|---|---|---|
| R1_rule2 | Rules / Rule 2 | 19–21 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/aadf0e11ed449a10f83b93e7c7164d5c812e8208/Reddit/Community%20Guidelines.md#L19-L21) |
| R1_rule3 | Rules / Rule 3 | 23–25 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/aadf0e11ed449a10f83b93e7c7164d5c812e8208/Reddit/Community%20Guidelines.md#L23-L25) |
| R1_rule5 | Rules / Rule 5 | 31–33 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/aadf0e11ed449a10f83b93e7c7164d5c812e8208/Reddit/Community%20Guidelines.md#L31-L33) |
| R1_rule6 | Rules / Rule 6 | 35–37 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/aadf0e11ed449a10f83b93e7c7164d5c812e8208/Reddit/Community%20Guidelines.md#L35-L37) |
| R1_rule8 | Rules / Rule 8 | 43–45 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/aadf0e11ed449a10f83b93e7c7164d5c812e8208/Reddit/Community%20Guidelines.md#L43-L45) |
| R1_enforcement | Enforcement | 47–57 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/aadf0e11ed449a10f83b93e7c7164d5c812e8208/Reddit/Community%20Guidelines.md#L47-L57) |
| R1_harassment | Разъяснение Rule 1 / harassment | 61–67 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/aadf0e11ed449a10f83b93e7c7164d5c812e8208/Reddit/Community%20Guidelines.md#L61-L67) |
| R1_spam | Разъяснение Rule 2 / spam | 114–152 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/aadf0e11ed449a10f83b93e7c7164d5c812e8208/Reddit/Community%20Guidelines.md#L114-L152) |
| R1_disruption | Разъяснение Rule 2 / disruptive behaviors | 156–196 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/aadf0e11ed449a10f83b93e7c7164d5c812e8208/Reddit/Community%20Guidelines.md#L156-L196) |
| R1_privacy | Разъяснение Rule 3 / personal information | 200–206 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/aadf0e11ed449a10f83b93e7c7164d5c812e8208/Reddit/Community%20Guidelines.md#L200-L206) |
| R1_impersonation | Разъяснение Rule 5 / impersonation | 268–318 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/aadf0e11ed449a10f83b93e7c7164d5c812e8208/Reddit/Community%20Guidelines.md#L268-L318) |
| R1_site | Разъяснение Rule 8 / normal use and API | 374–374 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/aadf0e11ed449a10f83b93e7c7164d5c812e8208/Reddit/Community%20Guidelines.md#L374-L374) |
| R2_rule2 | Rules / Rule 2 | 19–21 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L19-L21) |
| R2_rule3 | Rules / Rule 3 | 23–25 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L23-L25) |
| R2_rule5 | Rules / Rule 5 | 31–33 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L31-L33) |
| R2_rule6 | Rules / Rule 6 | 35–37 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L35-L37) |
| R2_rule8 | Rules / Rule 8 | 43–45 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L43-L45) |
| R2_enforcement | Enforcement | 47–57 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L47-L57) |
| R2_harassment | Разъяснение Rule 1 / harassment | 61–102 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L61-L102) |
| R2_spam | Разъяснение Rule 2 / spam | 223–260 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L223-L260) |
| R2_disruption | Разъяснение Rule 2 / disruptive behaviors | 264–304 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L264-L304) |
| R2_privacy | Разъяснение Rule 3 / personal information | 308–350 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L308-L350) |
| R2_impersonation | Разъяснение Rule 5 / impersonation | 459–497 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L459-L497) |
| R2_site | Разъяснение Rule 8 / normal use and API | 554–574 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/735fc4b354bddca24cac45f74c4a78184daae3fc/Reddit/Community%20Guidelines.md#L554-L574) |
| Y1_elections | Elections misinformation policies | 1670–1745 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/d6ddd0003c305ba46d51eada405888556cccc54b/YouTube/Community%20Guidelines.md#L1670-L1745) |
| Y2_elections | Elections misinformation policies | 1670–1741 | [Текст](https://github.com/OpenTermsArchive/pga-versions/blob/30e6af989d9b8656fddad0dbb4086b2efa3e3a0c/YouTube/Community%20Guidelines.md#L1670-L1741) |

## Как использовать для оценки

1. Загрузить указанные диапазоны четырёх фиксированных снимков. Сохранить commit SHA, service, document, section и evidence_id.
2. Проверить разметку вторым участником. Для вопросов без ответа проверить все диапазоны указанной редакции, а не только смежный фрагмент.
3. Передавать проверяемой системе вопрос и корпус. Поля reference_answer, expected_behavior и grading_note хранить отдельно от её входа.
4. Оценивать смысл обязательных фактов и правильность источников. Дословное совпадение с русским эталоном не требуется.
5. Для отдельной оценки Критика использовать critic_cases и фиксированную выдачу. Для полной системы разрешить собственный поиск по тому же корпусу.
6. Настраивать систему на development. Группы pseudonym и labels отмечены holdout_candidate; связанные вопросы должны оставаться в одной группе. Поскольку весь набор открыт разработчику, для слепой финальной оценки другой участник должен добавить ранее не показанные вопросы.

Для отвечаемых вопросов оценивать полноту обязательных фактов, отсутствие неподтверждённых утверждений и корректность пункта и редакции. Для Q23–Q27 оценивать обоснованное признание нехватки данных. Для Q28–Q30 — замечена ли неоднозначность. Для Критика отдельно учитывать пропуск недостаточной выдачи и ошибочную блокировку достаточной.

Прогонов моделей нет. Для метрики «найденные конфликты версий» сначала нужно согласовать определение конфликта и отдельно разметить положительные и отрицательные случаи. Изменение формулировки, уточнение и несовместимое утверждение должны иметь разные метки.

## Источник данных

Содержит сведения из [OpenTermsArchive/pga-versions](https://github.com/OpenTermsArchive/pga-versions), собранные Platform Governance Archive. База доступна по [ODC Attribution License](https://opendatacommons.org/licenses/by/1-0/). Пакет содержит русскую разметку и ссылки на исходные политики Reddit и YouTube.

