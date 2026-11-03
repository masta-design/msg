# -*- coding: utf-8 -*-
"""Библиотека секций прототипа МСГ. Каждая функция = одна секция (S01–S29, нумерация библиотеки)."""
import re

CFG = {'mode': 'multi'}
PHONE = '+7 804 700-02-24'
PHONE_TEL = '+78047000224'


def L(name, anchor=''):
    """Ссылка на страницу прототипа в зависимости от режима сборки."""
    if CFG['mode'] == 'spa':
        return '#/' + name
    return name + '.html' + (('#' + anchor) if anchor else '')


def M(tab='buy', service=None, tariff=None):
    a = ' data-modal data-modal-tab="%s"' % tab
    if service:
        a += ' data-modal-service="%s"' % service
    if tariff:
        a += ' data-modal-tariff="%s"' % tariff
    return a


_SUB_RE = re.compile(r'(<p class="(?:lead|muted)[^"]*"[^>]*>|</h[1-6]>\s*<p(?: [^>]*)?>)(.*?)(</p>)', re.S)


def no_dot(html):
    """Правило: подзаголовок из одного предложения — без точки в конце. Подзаголовок — это p.lead, p.muted
    и любой абзац сразу после заголовка (h1–h6). Применяется при сборке ко всему HTML;
    если в тексте несколько предложений, точки остаются."""
    def fix(m):
        inner = m.group(2).rstrip()
        text = re.sub(r'<[^>]+>', '', inner)
        if inner.endswith('.') and not inner.endswith('..') and not re.search(r'[.!?…]\s+\S', text[:-1]):
            inner = inner[:-1]
        return m.group(1) + inner + m.group(3)
    return _SUB_RE.sub(fix, html)


def ph(label, ratio='16x9', cls='', kind='Изображение'):
    r = (' r-' + ratio) if ratio else ''
    return '<div class="ph%s %s"><span>%s: %s</span></div>' % (r, cls, kind, label)


def head(title, lead=None, kicker=None, right=None, tag='h2'):
    k = '<p class="kicker">%s</p>' % kicker if kicker else ''
    l = '<p class="lead">%s</p>' % lead if lead else ''
    r = right or ''
    return '<div class="sec-head"><div>%s<%s>%s</%s>%s</div>%s</div>' % (k, tag, title, tag, l, r)


def sec(inner, id=None, alt=False, h=None):
    cls = 'sec' + (' alt' if alt else '')
    i = ' id="%s"' % id if id else ''
    return '<section class="%s"%s><div class="wrap">%s%s</div></section>' % (cls, i, h or '', inner)


def btn(text, href='#', kind='primary', attrs='', sm=False):
    s = ' btn-sm' if sm else ''
    return '<a class="btn btn-%s%s" href="%s"%s>%s</a>' % (kind, s, href, attrs, text)


def check_list(items, cls='check'):
    return '<ul class="%s">%s</ul>' % (cls, ''.join('<li>%s</li>' % i for i in items))


def slider_nav():
    # пагинация слева, стрелки справа
    return ('<div class="slider-nav"><div class="dots"></div><div class="slider-arrows">'
            '<button class="slider-btn slider-prev" aria-label="Назад">←</button>'
            '<button class="slider-btn slider-next" aria-label="Вперёд">→</button></div></div>')


# ------------------------------------------------------------------ S01 Hero
def hero_media(label, ratio, video=None):
    """Медиа hero: изображение-заглушка или видео. video = 'click' (запуск по кнопке play) или 'auto' (автовоспроизведение без звука)."""
    if not video:
        return ph(label, ratio)
    r = (' r-' + ratio) if ratio else ''
    if video == 'auto':
        inner = '<span>Видео: %s — автовоспроизведение без звука, по кругу</span>' % label
    else:
        inner = '<div><div class="ph-play" role="button" tabindex="0" aria-label="Смотреть видео">▶</div><span>Видео: %s — запуск по клику</span></div>' % label
    return '<div class="ph%s hero-video" data-video="%s">%s</div>' % (r, video, inner)


def hero(variant='A', h1='', lead=None, bullets=None, buttons=None, img=None, price=None, video=None):
    l = '<p class="lead">%s</p>' % lead if lead else ''
    bl = check_list(bullets) if bullets else ''
    # вариант C — компактный, только заголовок и подзаголовок, без кнопок
    bt = '<div class="btns">%s</div>' % ''.join(buttons) if buttons and variant != 'C' else ''
    if variant == 'D':
        # вариант D — текст, стоимость и изображение; price = (подпись, значение)
        pr = ('<div class="hero-price"><span class="caption">%s</span>'
              '<div class="tariff-price">%s</div></div>' % price) if price else ''
        note = '<p class="caption hero-note">%s</p>' % PRICE_NOTE if price else ''
        body = '<div class="hero-body"><h1>%s</h1>%s%s%s%s%s</div>' % (h1, l, bl, pr, bt, note)
        return '<section class="hero"><div class="wrap hero-a">%s%s</div></section>' % (body, hero_media(img, '4x3', video))
    body = '<div class="hero-body"><h1>%s</h1>%s%s%s</div>' % (h1, l, bl, bt)
    if variant == 'A':
        return '<section class="hero"><div class="wrap hero-a">%s%s</div></section>' % (body, hero_media(img, '4x3', video))
    if variant == 'B':
        # изображение на всю ширину экрана, карточка с текстом — в рамках контента
        return ('<section class="hero hero-bleed"><div class="hero-b">%s<div class="wrap"><div class="hero-card">%s</div></div></div></section>'
                % (hero_media(img, None, video), body))
    return '<section class="hero hero-c"><div class="wrap">%s</div></section>' % body


# ------------------------------------------------------------------ Подменю
def subnav(items, service=None):
    links = ''.join('<a class="sn" href="#%s">%s</a>' % (a, t) for a, t in items)
    return '<nav class="subnav" aria-label="Разделы страницы"><div class="wrap">%s</div></nav>' % links


# ------------------------------------------------------------------ S08 Карточки услуг
def svc_card(c, cat_attr=False):
    cat = '<div class="svc-top"><span class="caption">%s</span></div>' % c['cat'] if c.get('cat') else ''

    price = '<div class="svc-foot"><span class="price">%s</span></div>' % c['price'] if c.get('price') else ''
    img = ph(c['img'], '3x2') if c.get('img') else ''
    da = ' data-cat="%s"' % c['catkey'] if cat_attr else ''
    return ('<a class="card svc" href="%s"%s>%s<div class="svc-body">%s<h3>%s</h3><p class="muted">%s</p>%s</div></a>'
            % (c['href'], da, img, cat, c['title'], c['desc'], price))


def services_grid(items, cols=3, variant='grid', h=None, id=None, alt=False, note=None):
    cols = min(cols, 3)  # сетка в 4 колонки не используется
    cards = ''.join(svc_card(c) for c in items)
    n = '<p class="note-foot">%s</p>' % note if note else ''
    if variant == 'slider':
        inner = '<div class="slider"><div class="slider-track">%s</div>%s</div>%s' % (cards, slider_nav(), n)
    else:
        inner = '<div class="grid g%d">%s</div>%s' % (cols, cards, n)
    return sec(inner, id=id, alt=alt, h=h)


def svc_card_h(c):
    """Горизонтальная карточка сервиса: слева изображение 3:2, справа информация."""
    img = ph(c['img'], '3x2') if c.get('img') else ''
    price = '<div class="svc-foot"><span class="price">%s</span></div>' % c['price'] if c.get('price') else ''
    return ('<a class="card svc svc-h" href="%s">%s<div class="svc-body"><h3>%s</h3><p class="muted">%s</p>%s</div></a>'
            % (c['href'], img, c['title'], c['desc'], price))


def _svc_group(title, lead, items, href='#'):
    cards = ''.join(svc_card_h(c) for c in items)
    # href=None — заголовок без ссылки (когда группа показана на странице самого направления)
    h2 = ('<h2><a href="%s">%s<span class="arrow" aria-hidden="true"> →</span></a></h2>' % (href, title)) if href is not None else ('<h2>%s</h2>' % title if title else '')
    # заголовок и подзаголовок необязательны: без них секция состоит только из карточек
    head = ('<div class="svc-group-head">%s%s</div>' % (h2 if title else '', '<p class="lead">%s</p>' % lead if lead else '')) if (title or lead) else ''
    return '<div class="svc-group">%s<div class="svc-stack">%s</div></div>' % (head, cards)


def services_groups(groups, id=None, alt=False, note=None):
    """S08-C: одна секция с несколькими группами. Группа: заголовок направления и подзаголовок сверху,
    под ними горизонтальные карточки сервисов в две колонки. groups = [(title, lead, items, href), ...]."""
    n = '<p class="note-foot center">%s</p>' % note if note else ''
    return sec(''.join(_svc_group(*g) for g in groups) + n, id=id, alt=alt)


def services_group(title, lead, items, href='#', id=None, alt=False, note=None):
    """Одна группа сервисов в отдельной секции."""
    return services_groups([(title, lead, items, href)], id=id, alt=alt, note=note)


# ------------------------------------------------------------------ S03 Изображение + текст
def img_text(title, paras, img, bullets=None, kicker=None, button=None, id=None, alt=False):
    k = '<p class="kicker">%s</p>' % kicker if kicker else ''
    p = ''.join('<p>%s</p>' % x for x in paras)
    bl = check_list(bullets) if bullets else ''
    b = button or ''
    inner = ('<div class="it"><div class="it-media">%s</div><div class="it-body">%s<h2>%s</h2>%s%s%s</div></div>'
             % (ph(img, '4x3'), k, title, p, bl, b))
    return sec(inner, id=id, alt=alt)


# ------------------------------------------------------------------ S09 Что входит
def includes(items, cols=4, h=None, note=None, id=None, alt=False, img=None):
    out = ''
    for it in items:
        icon, title = it[0], it[1]
        desc = it[2] if len(it) > 2 else None
        if isinstance(desc, (list, tuple)):  # перечень пунктов в карточке
            body = '<ul>%s</ul>' % ''.join('<li>%s</li>' % x for x in desc)
        else:
            body = '<p>%s</p>' % desc if desc else ''
        out += '<div class="card inc"><span class="ico">%s</span><h4>%s</h4>%s</div>' % (icon, title, body)
    n = '<p class="note-foot">%s</p>' % note if note else ''
    # img — широкая картинка 21:9 над сеткой
    top = ph(img, '21x9') if img else ''
    grid = '<div class="grid g%d">%s</div>' % (cols, out)
    if img:
        grid = '<div class="inc-wide">%s%s</div>' % (top, grid)
    return sec('%s%s' % (grid, n), id=id, alt=alt, h=h)


# ------------------------------------------------------------------ Сноска о ценах (обязательна везде, где показана цена)
PRICE_NOTE = ('* Цены указаны ориентировочно. Стоимость может отличаться в зависимости от региона и канала продажи — '
              'уточняйте у менеджера.')


# ------------------------------------------------------------------ S12 Таблица сравнения
def compare_table(cols, rows, total=None, h=None, note=None, id=None, alt=False, buttons=None):
    th = '<th>Услуга</th>' + ''.join('<th>%s</th>' % c for c in cols)
    body = ''
    for r in rows:
        if isinstance(r, str):
            body += '<tr class="grp"><td colspan="%d">%s</td></tr>' % (len(cols) + 1, r)
            continue
        cells = '<td>%s</td>' % r[0]
        for c in r[1:]:
            if c is None:
                continue
            if isinstance(c, dict):
                cells += '<td rowspan="%d">%s</td>' % (c['span'], c['t'])
            elif c is True:
                cells += '<td class="y">✓</td>'
            elif c is False:
                cells += '<td class="n">—</td>'
            else:
                cells += '<td>%s</td>' % c
        body += '<tr>%s</tr>' % cells
    if total:
        body += '<tr class="total"><td>%s</td>%s</tr>' % (total[0], ''.join('<td>%s</td>' % x for x in total[1:]))
    if buttons:
        body += '<tr class="act"><td></td>%s</tr>' % ''.join('<td>%s</td>' % x for x in buttons)
    n = '<p class="note-foot">%s</p>' % note if note else ''
    inner = '<div class="tbl-wrap"><table class="tbl"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>%s' % (th, body, n)
    return sec(inner, id=id, alt=alt, h=h)


# ------------------------------------------------------------------ S11 Детальное описание
def details_list(items, h=None, single=True, note=None, id=None, alt=False, variant='A'):
    if variant == 'B':
        rows = ''
        for icon, title, summ, body in items:
            rows += ('<div class="dl-row"><div class="dl-head">%s<h4>%s</h4>%s</div><div class="dl-body">%s</div></div>'
                     % (('<span class="ico">%s</span>' % icon) if icon else '', title,
                        '<span class="sum">%s</span>' % summ if summ else '', body))
        n = '<p class="note-foot">%s</p>' % note if note else ''
        return sec('<div class="dlist">%s</div>%s' % (rows, n), id=id, alt=alt, h=h)
    out = ''
    for i, it in enumerate(items):
        icon, title, summ, body = it
        o = ' open' if i == 0 else ''
        out += ('<details%s><summary>%s<span>%s</span>%s</summary><div class="acc-body">%s</div></details>'
                % (o, ('<span class="ico" style="font-size:22px">%s</span>' % icon) if icon else '', title,
                   '<span class="sum">%s</span>' % summ if summ else '', body))
    s = ' data-single' if single else ''
    n = '<p class="note-foot">%s</p>' % note if note else ''
    return sec('<div class="acc"%s>%s</div>%s' % (s, out, n), id=id, alt=alt, h=h)


# ------------------------------------------------------------------ S10 Ситуации
def situations(items, cols=3, h=None, id=None, alt=False, note=None):
    out = ''
    for icon, title, lst in items:
        out += ('<div class="card sit"><div class="sit-head"><span class="ico">%s</span><h4>%s</h4></div>%s</div>'
                % (icon, title, check_list(lst)))
    n = '<p class="note-foot">%s</p>' % note if note else ''
    return sec('<div class="grid g%d">%s</div>%s' % (cols, out, n), id=id, alt=alt, h=h)


# ------------------------------------------------------------------ S05 О компании
def about_company(title, paras, img, id=None, alt=False):
    """Текст слева, одно изображение 3:2 справа: заголовок и описание."""
    p = ''.join('<p>%s</p>' % x for x in paras)
    inner = ('<div class="about"><div class="it-body"><h2>%s</h2>%s</div><div class="about-media">%s</div></div>'
             % (title, p, ph(img, '3x2')))
    return sec(inner, id=id, alt=alt)


# ------------------------------------------------------------------ S04 Заголовок + текст + карточки
def intro_cards(title, paras, cards, button=None, link=None, cols=2, id=None, alt=False):
    """Вверху заголовок слева и текст с кнопкой и ссылкой справа, ниже карточки (иконка, заголовок, описание)."""
    p = ''.join('<p>%s</p>' % x for x in paras)
    acts = '<div class="btns">%s%s</div>' % (button or '', link or '') if (button or link) else ''
    top = '<div class="ic-top"><h2>%s</h2><div class="ic-text">%s%s</div></div>' % (title, p, acts)
    cs = ''.join('<div class="card ic-card"><span class="ico">%s</span><div><h3>%s</h3><p>%s</p></div></div>' % c for c in cards)
    return sec('%s<div class="grid g%d">%s</div>' % (top, cols, cs), id=id, alt=alt)


# ------------------------------------------------------------------ S14 Шаги с картинками
def steps_image(title, lead, items, id=None, alt=False):
    """Вертикальный пошаговый список: линия по центру, картинка и текст чередуются слева и справа. items = [(заголовок, описание, картинка)]."""
    rows = ''
    for i, (t, d, img) in enumerate(items, 1):
        media = '<div class="tl-media">%s</div>' % ph(img, '3x2')
        text = '<div class="tl-text"><h3>%s</h3><p>%s</p></div>' % (t, d)
        left, right = (media, text) if i % 2 else (text, media)
        rows += '<div class="tl-row">%s<span class="step-n">%02d</span>%s</div>' % (left, i, right)
    head_ = ('<div class="sec-head sh-center"><div><h2>%s</h2>%s</div></div>'
             % (title, '<p class="lead">%s</p>' % lead if lead else ''))
    return sec('<div class="tl">%s</div>' % rows, id=id, alt=alt, h=head_)


# ------------------------------------------------------------------ S13 Шаги
def steps(items, h=None, vertical=False, id=None, alt=False):
    out = ''
    for i, (t, d) in enumerate(items, 1):
        if vertical:
            out += '<div class="step"><span class="step-n">%d</span><div><h4>%s</h4><p>%s</p></div></div>' % (i, t, d)
        else:
            out += '<div class="step"><span class="step-n">%d</span><h4>%s</h4><p>%s</p></div>' % (i, t, d)
    return sec('<div class="steps%s">%s</div>' % (' vert' if vertical else '', out), id=id, alt=alt, h=h)


# ------------------------------------------------------------------ S15 Преимущества
def advantages(items, h=None, id=None, alt=False):
    cards = ''.join('<div class="adv"><span class="ico">%s</span><h4>%s</h4><p>%s</p></div>' % i for i in items)
    return sec('<div class="grid g%d">%s</div>' % (min(len(items), 4), cards), id=id, alt=alt, h=h)


# ------------------------------------------------------------------ S16 Цифры
def stats(items, h=None, id=None, alt=True, note=None):
    out = ''.join('<div class="stat"><b>%s</b><span>%s</span></div>' % i for i in items)
    n = '<p class="note-foot">%s</p>' % note if note else ''
    return sec('<div class="stats g%d" style="display:grid">%s</div>%s' % (len(items), out, n), id=id, alt=alt, h=h)


# ------------------------------------------------------------------ S17 Кейс-карточки
def case_card(c):
    """Карточка находки: изображение 3:2, заголовок, стоимость работ, затем рекомендация и риски."""
    cost = ('<p class="case-cost"><span>Стоимость работ</span><b>%s</b></p>' % c['cost']) if c.get('cost') else ''
    return ('<article class="card case">%s<div class="case-body"><h4>%s</h4>%s'
            '<div><h5>Рекомендация</h5><p>%s</p></div><div><h5>Риски</h5><p>%s</p></div></div></article>'
            % (ph(c['img'], '3x2'), c['title'], cost, c['rec'], c['risk']))


def cases(items, h=None, id=None, alt=False):
    """До трёх карточек — сеткой, больше — слайдером с тремя карточками в ряду."""
    cards = ''.join(case_card(c) for c in items)
    if len(items) > 3:
        inner = ('<div class="slider"><div class="slider-track" style="grid-auto-columns:calc((100%% - 48px)/3)">%s</div>%s</div>'
                 % (cards, slider_nav()))
    else:
        inner = '<div class="grid g%d">%s</div>' % (len(items), cards)
    return sec(inner, id=id, alt=alt, h=h)

# ------------------------------------------------------------------ S20 География
def geography(cities, title, lead, note=None, id=None, alt=False):
    """Список городов на всю ширину; больше 40 городов — кнопка «Показать все»."""
    many = len(cities) > 40
    lis = ''.join('<li>%s</li>' % c for c in cities)
    more = ('<button class="btn btn-secondary btn-sm" data-more style="margin-top:24px">Показать все города (%d)</button>' % len(cities)
            if many else '')
    n = '<p class="note-foot">%s</p>' % note if note else ''
    return sec('<div class="geo-wrap"><ul class="plain cities cities-lg%s">%s</ul>%s%s</div>' % (' more' if many else '', lis, more, n),
               id=id, alt=alt, h=head(title, lead))


# ------------------------------------------------------------------ S24 Галерея
def gallery(items, variant='B', h=None, id=None, alt=False, cols=4):
    if variant == 'A':
        slides = ''.join('<figure class="gal-item">%s<figcaption>%s</figcaption></figure>' % (ph(i, '21x9'), c) for i, c in items)
        thumbs = ''.join('<button aria-label="Слайд %d">%s</button>' % (k + 1, ph(i, '4x3')) for k, (i, c) in enumerate(items))
        inner = ('<div><div class="slider one"><div class="slider-track">%s</div>%s</div><div class="gal-thumbs">%s</div></div>'
                 % (slides, slider_nav(), thumbs))
    else:
        inner = '<div class="grid g%d">%s</div>' % (cols, ''.join(
            '<figure class="gal-item">%s<figcaption>%s</figcaption></figure>' % (ph(i, '4x3'), c) for i, c in items))
    return sec(inner, id=id, alt=alt, h=h)


# ------------------------------------------------------------------ S25 Видео
def video(label, title, desc=None, points=None, variant='split', id=None, alt=False):
    v = ('<div class="video"><div class="ph r-16x9"><div><div class="ph-play">▶</div><span>Видео: %s</span></div></div></div>' % label)
    d = '<p class="muted">%s</p>' % desc if desc else ''
    p = check_list(points) if points else ''
    if variant == 'wide':
        return sec(v, id=id, alt=alt, h=head(title, desc))
    inner = '<div class="video-split">%s<div class="it-body"><h2>%s</h2>%s%s</div></div>' % (v, title, d, p)
    return sec(inner, id=id, alt=alt)


# ------------------------------------------------------------------ S18 Отзывы
def reviews(items, h=None, csi=None, id=None, alt=False, demo=True):
    out = ''
    for r in items:
        name, city, svc, text, date = r
        ini = ''.join(x[0] for x in name.split()[:2])
        out += ('<article class="card rev"><div class="rev-who"><span class="ava">%s</span><div><b>%s</b><div class="caption">%s</div></div></div>'
                '<div class="stars">★★★★★</div><p>%s</p><div class="caption">%s · %s%s</div></article>'
                % (ini, name, city, text, svc, date, ' · демо' if demo else ''))
    return sec('<div class="slider"><div class="slider-track">%s</div>%s</div>' % (out, slider_nav()), id=id, alt=alt, h=h)


# ------------------------------------------------------------------ S21 FAQ
def faq(items, h=None, id=None, alt=False, service=None):
    out = ''.join('<details%s><summary><span>%s</span></summary><div class="acc-body"><p>%s</p></div></details>'
                  % (' open' if i == 0 else '', q, a) for i, (q, a) in enumerate(items))
    ask = ('<aside class="ask"><span class="ico">💬</span><h4>Не нашли ответ?</h4><p class="muted">Задайте вопрос — специалист ответит '
           'по телефону или в мессенджере.</p>%s</aside>' % btn('Задать вопрос', '#', 'primary', M('buy', service)))
    return sec('<div class="faq-grid"><div class="acc" data-single>%s</div>%s</div>' % (out, ask), id=id, alt=alt, h=h)


# ------------------------------------------------------------------ S22 Документы
def documents(items, h=None, id=None, alt=False):
    """Компактные карточки-ссылки в 3 колонки: значок, название, формат и редакция, «Скачать»."""
    cards = ''.join('<a class="card doc" href="#"><span class="ico">📄</span><b>%s</b><span class="meta">%s</span>'
                    '<span class="doc-dl">Скачать</span></a>' % d for d in items)
    return sec('<div class="grid g3 docs">%s</div>' % cards, id=id, alt=alt, h=h)


# ------------------------------------------------------------------ S23 Файлы и документы
def file_list(items, h=None, id=None, alt=False):
    """Документы разных форматов (1–5 шт.). Карточка целиком — ссылка, файл открывается в новой вкладке.
    items = [dict(title, caption, type, size, date, href='#')], дата в формате дд.мм.гггг."""
    cards = ''
    for f in items:
        cards += ('<a class="card file" href="%s" target="_blank" rel="noopener">'
                  '<span class="file-type">%s</span>'
                  '<span class="file-body"><span class="file-title">%s</span><p class="muted small">%s</p>'
                  '<span class="file-meta">%s · %s</span></span></a>'
                  % (f.get('href', '#'), f['type'], f['title'], f['caption'], f['size'], f['date']))
    return sec('<div class="grid g2">%s</div>' % cards, id=id, alt=alt, h=h)


# ------------------------------------------------------------------ Форма (G04 + S26)
def form_fields(service=None, modal=False):
    cert = ('<div class="field only-cert"><label>Номер сертификата</label><input name="cert" placeholder="Например, ДС-000123"></div>'
            if modal else '')
    # согласие и политика — разные документы; открываются в новой вкладке, чтобы не терять заполненную форму
    doc = lambda text, page: '<a href="%s" target="_blank" rel="noopener">%s</a>' % (L(page), text)
    agree = ('<label class="agree"><input type="checkbox" required> <span>Даю %s в соответствии с %s</span></label>'
             % (doc('согласие на обработку персональных данных', 'consent'), doc('Политикой обработки персональных данных', 'privacy')))
    return ('<form class="form" novalidate>'
            '<div class="row2"><div class="field"><label>Имя <i>*</i></label><input name="name" required autocomplete="name"></div>'
            '<div class="field"><label>Телефон <i>*</i></label><input name="phone" type="tel" placeholder="+7 ___ ___-__-__" required></div></div>'
            '<div class="field"><label>E-mail</label><input name="email" type="email" placeholder="name@mail.ru"></div>%s'
            '<div class="field"><label>Комментарий</label><textarea name="comment" placeholder="Опишите ситуацию или вопрос"></textarea></div>'
            '%s<button class="btn btn-primary btn-block" type="submit">Отправить заявку</button>%s</form>'
            '<div class="success"><span class="ok">✓</span><h3>Заявка принята</h3><p class="muted">Свяжемся с вами в течение 30 минут в рабочее время.</p>'
            '<button class="btn btn-secondary" type="button" %s>%s</button></div>'
            % (cert, agree,
               ('<p class="form-hint">Срочная помощь по сертификату — <a href="tel:%s">%s</a>, круглосуточно</p>' % (PHONE_TEL, PHONE)) if modal else '',
               'data-close' if modal else 'data-reset', 'Закрыть' if modal else 'Отправить ещё одну'))


def modal_html():
    return ('<div class="modal" id="modal" role="dialog" aria-modal="true" aria-labelledby="modal-t"><div class="modal-box">'
            '<button class="modal-x" aria-label="Закрыть">×</button><h3 id="modal-t">Оставить заявку</h3>'
            '<p class="muted" style="margin-top:6px">Перезвоним, ответим на вопросы и поможем подобрать сервис</p>'
            '<div class="mtabs" role="tablist"><button data-mtab="buy" class="is-active">Хочу подключить сервис</button>'
            '<button data-mtab="cert">Уже есть сертификат</button><button data-mtab="partner">Партнёрство</button></div>'
            '<div class="form-wrap" style="margin-top:20px">%s</div></div></div>' % form_fields(modal=True))


def lead_form(title, text, bullets=None, service=None, id='form', alt=True):
    b = check_list(bullets) if bullets else ''
    inner = ('<div class="lead-sec"><div class="it-body"><h2>%s</h2><p class="lead">%s</p>%s'
             '<div class="phone-box"><a class="phone-big" href="tel:%s">%s</a><span class="caption">Круглосуточно, бесплатно по России</span></div></div>'
             '<div class="card form-card form-wrap">%s</div></div>' % (title, text, b, PHONE_TEL, PHONE, form_fields(service)))
    return sec(inner, id=id, alt=alt)


# ------------------------------------------------------------------ S27 CTA
def cta(title, sub=None, button=None, phone=True, icon=None, id=None, alt=False):
    i = '<span class="ico">%s</span>' % icon if icon else ''
    s = '<p class="muted">%s</p>' % sub if sub else ''
    p = '<a class="tel" href="tel:%s">%s</a>' % (PHONE_TEL, PHONE) if phone else ''
    inner = ('<div class="cta">%s<div class="cta-body"><h3>%s</h3>%s</div>%s%s</div>'
             % (i, title, s, p, button or ''))
    return sec(inner, id=id, alt=alt)


# ------------------------------------------------------------------ S28 Сертификат
def cert_block(service=None, id='cert', alt=False):
    st = [('Позвоните или оставьте заявку', 'Колл-центр работает круглосуточно, без выходных.'),
          ('Назовите номер сертификата', 'Он указан в письме, которое пришло после покупки.'),
          ('Специалист решит вопрос', 'Свяжется с вами, согласует время и организует помощь.')]
    s = ''.join('<div><span class="step-n">%d</span><div><h4>%s</h4><p class="muted small">%s</p></div></div>' % (i, a, b)
                for i, (a, b) in enumerate(st, 1))
    inner = ('<div class="cert"><div class="it-body"><h2>Уже есть сертификат МСГ?</h2>'
             '<a class="phone-big" href="tel:%s">%s</a><span class="caption">Круглосуточно, бесплатно по России</span>'
             '<div class="btns">%s</div></div>'
             '<div class="cert-steps">%s</div></div>'
             % (PHONE_TEL, PHONE, btn('Оставить заявку', '#', 'primary', M('cert', service)), s))
    return sec(inner, id=id, alt=alt)


# ------------------------------------------------------------------ S29 Партнёрам
def partner_block(title, lead, points, id=None, alt=False, kicker='Для бизнеса'):
    pts = ''.join('<div class="pt"><span class="ico">%s</span><div><h4>%s</h4><p>%s</p></div></div>' % p for p in points)
    inner = ('<div class="partner"><div class="it-body"><p class="kicker">%s</p><h2>%s</h2><p class="lead">%s</p>'
             '<div class="btns">%s%s</div></div><div class="grid">%s</div></div>'
             % (kicker, title, lead, btn('Стать партнёром', '#', 'primary', M('partner')),
                btn('Подробнее', L('stub'), 'secondary'), pts))
    return sec(inner, id=id, alt=alt)


# ------------------------------------------------------------------ S02 Промо-слайдер
def promo(banners, id=None, alt=False):
    out = ''
    for b in banners:
        out += ('<div class="promo"><div class="promo-body"><h2>%s</h2><p class="lead">%s</p>%s</div>%s</div>'
                % (b['title'], b['text'], b['button'], ph(b['img'], '4x3')))
    return sec('<div class="slider one"><div class="slider-track">%s</div>%s</div>' % (out, slider_nav()), id=id, alt=alt)


# ------------------------------------------------------------------ S19 Наши партнёры
def partners_slider(title, lead, logos, id=None, alt=False):
    """Автопрокручивающаяся лента логотипов партнёров. logos — подписи заглушек; лента дублируется для бесшовного цикла."""
    def group(hidden=False):
        items = ''.join('<div class="p-logo">%s</div>' % ph(l, None, '', kind='Лого') for l in logos)
        return '<div class="logos-group"%s>%s</div>' % (' aria-hidden="true"' if hidden else '', items)
    inner = '<div class="logos" aria-label="Логотипы партнёров"><div class="logos-track">%s%s</div></div>' % (group(), group(True))
    return sec(inner, id=id, alt=alt, h=head(title, lead))


# ------------------------------------------------------------------ S06 Текст
def rich_text(html, id=None, alt=False):
    return sec('<div class="rich">%s</div>' % html, id=id, alt=alt)


# ------------------------------------------------------------------ S07 Текст с изображением
def rich_media(html, img, side='left', id=None, alt=False):
    """Форматированный текст и изображение 50 на 50. side: 'left' — картинка слева, 'right' — картинка справа."""
    media = '<div class="rm-media">%s</div>' % ph(img, '4x3')
    text = '<div class="rich rm-text">%s</div>' % html
    cells = media + text if side == 'left' else text + media
    return sec('<div class="rm">%s</div>' % cells, id=id, alt=alt)


# ------------------------------------------------------------------ Примечание (внутри текстовой секции)
def note_block(text, variant='info', link=None):
    i = 'ℹ︎' if variant == 'info' else '⚠︎'
    lk = ' <a href="%s">%s</a>' % link if link else ''
    return '<div class="note%s"><span class="ico">%s</span><span>%s%s</span></div>' % (' warn' if variant == 'warn' else '', i, text, lk)


# ------------------------------------------------------------------ Аннотация для P7
def ann(bid, name, purpose, variants, settings, used, anchor):
    return ('<div class="ann" id="%s"><div class="wrap"><div class="ann-box"><div><span class="id">%s</span><b>%s</b><span>%s</span></div>'
            '<div><b>Варианты</b><span>%s</span></div><div><b>Настройки</b><span>%s</span></div>'
            '<div><b>Где используется</b><span>%s</span></div></div></div></div>'
            % (anchor, bid, name, purpose, variants, settings, used))
