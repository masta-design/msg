const catalogItems = [
  { title: "Все услуги", category: "Каталог", url: "index.html" },
  { title: "Сервисы для дома", category: "Направление", url: "life-services.html" },
  { title: "Домовой сервис", category: "Дом", url: "financial-protector.html" },
  { title: "Чекап квартиры", category: "Недвижимость", url: "life-services.html#products" },
  { title: "Приёмка квартиры", category: "Недвижимость", url: "life-services.html#products" },
  { title: "Электрик", category: "Домовой сервис", url: "financial-protector.html#composition" },
  { title: "Сантехник", category: "Домовой сервис", url: "financial-protector.html#composition" },
  { title: "Мастер на час", category: "Домовой сервис", url: "financial-protector.html#composition" },
  { title: "Сервисы для авто", category: "Направление", url: "index.html#directions" },
  { title: "Техпомощь", category: "Авто", url: "index.html#popular" },
  { title: "Сервисы для недвижимости", category: "Направление", url: "index.html#directions" },
  { title: "Домовой сервис", category: "Недвижимость", url: "financial-protector.html" },
  { title: "Приёмка квартиры", category: "Недвижимость", url: "index.html#popular" }
];

const searchInputs = document.querySelectorAll("[data-catalog-search]");

searchInputs.forEach((input) => {
  const container = input.closest(".catalog-search");
  const results = container?.querySelector(".search-results");
  if (!results) return;

  const renderResults = () => {
    const query = input.value.trim().toLocaleLowerCase("ru");
    if (!query) {
      results.classList.remove("is-open");
      results.innerHTML = "";
      return;
    }

    const matches = catalogItems
      .filter((item) => `${item.title} ${item.category}`.toLocaleLowerCase("ru").includes(query))
      .slice(0, 6);

    results.innerHTML = matches.length
      ? matches.map((item) => `
          <a class="search-result" href="${item.url}">
            <span>${item.title}</span>
            <small>${item.category}</small>
          </a>
        `).join("")
      : '<div class="search-empty">Ничего не найдено. Попробуйте описать задачу иначе.</div>';
    results.classList.add("is-open");
  };

  input.addEventListener("input", renderResults);
  input.addEventListener("focus", renderResults);

  document.addEventListener("click", (event) => {
    if (!container.contains(event.target)) results.classList.remove("is-open");
  });
});

document.addEventListener("keydown", (event) => {
  if (event.key === "/" && !["INPUT", "TEXTAREA"].includes(document.activeElement.tagName)) {
    event.preventDefault();
    searchInputs[0]?.focus();
  }
  if (event.key === "Escape") {
    document.querySelectorAll(".search-results").forEach((result) => result.classList.remove("is-open"));
  }
});

const menuToggle = document.querySelector("[data-menu-toggle]");
menuToggle?.addEventListener("click", () => {
  const isOpen = document.body.classList.toggle("menu-open");
  menuToggle.setAttribute("aria-expanded", String(isOpen));
  menuToggle.textContent = isOpen ? "×" : "☰";
});

document.querySelectorAll(".header-nav a").forEach((link) => {
  link.addEventListener("click", () => {
    document.body.classList.remove("menu-open");
    menuToggle?.setAttribute("aria-expanded", "false");
    if (menuToggle) menuToggle.textContent = "☰";
  });
});

const placeholderLinks = document.querySelectorAll("[data-placeholder-link]");
if (placeholderLinks.length) {
  const toast = document.createElement("div");
  toast.className = "demo-toast";
  toast.textContent = "Этот раздел обозначен в навигации, но не входит в текущий демо-прототип.";
  document.body.appendChild(toast);
  let toastTimer;

  placeholderLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      toast.classList.add("is-visible");
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => toast.classList.remove("is-visible"), 2400);
    });
  });
}

const recommendationData = {
  fraud: {
    title: "Домовой сервис",
    text: "Помощь проверенных специалистов для решения бытовых задач дома.",
    url: "financial-protector.html"
  },
  legal: {
    title: "Чекап квартиры",
    text: "Техническая проверка жилья перед покупкой, арендой или ремонтом.",
    url: "life-services.html#products"
  },
  road: {
    title: "Техпомощь",
    text: "Одна точка входа для помощи в экстренной ситуации на дороге.",
    url: "index.html#popular"
  },
  home: {
    title: "Домовой сервис",
    text: "Проверенные специалисты для решения бытовых проблем владельцев недвижимости.",
    url: "index.html#popular"
  }
};

document.querySelectorAll("[data-scenario]").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll("[data-scenario]").forEach((item) => item.classList.remove("is-active"));
    button.classList.add("is-active");
    const data = recommendationData[button.dataset.scenario];
    const recommendation = document.querySelector("[data-recommendation]");
    if (!data || !recommendation) return;
    recommendation.querySelector("[data-recommendation-title]").textContent = data.title;
    recommendation.querySelector("[data-recommendation-text]").textContent = data.text;
    recommendation.querySelector("a").href = data.url;
    recommendation.classList.add("is-visible");
  });
});

document.querySelectorAll("[data-tariff]").forEach((button) => {
  button.addEventListener("click", () => {
    const card = button.closest(".tariff-card");
    document.querySelectorAll(".tariff-card").forEach((item) => item.classList.remove("is-selected"));
    card?.classList.add("is-selected");
    const output = document.querySelector("[data-selected-tariff]");
    if (output) output.textContent = button.dataset.tariff;
  });
});

document.querySelectorAll("[data-gallery]").forEach((gallery) => {
  const track = gallery.querySelector(".gallery-track");
  const slides = gallery.querySelectorAll(".gallery-slide");
  let index = 0;

  const update = () => {
    track.style.transform = `translateX(-${index * 100}%)`;
  };

  gallery.querySelector("[data-gallery-prev]")?.addEventListener("click", () => {
    index = (index - 1 + slides.length) % slides.length;
    update();
  });

  gallery.querySelector("[data-gallery-next]")?.addEventListener("click", () => {
    index = (index + 1) % slides.length;
    update();
  });
});

document.querySelectorAll("[data-service-slider]").forEach((slider) => {
  const viewport = slider.querySelector("[data-service-viewport]");
  const previous = slider.querySelector("[data-service-prev]");
  const next = slider.querySelector("[data-service-next]");
  const leftFade = slider.querySelector(".service-strip__fade--left, [data-slider-left-fade]");
  if (!viewport) return;

  const updateArrows = () => {
    const maxScroll = viewport.scrollWidth - viewport.clientWidth;
    const isAtStart = viewport.scrollLeft <= 2;
    if (previous) previous.hidden = isAtStart;
    if (leftFade) leftFade.hidden = isAtStart;
    if (next) next.disabled = viewport.scrollLeft >= maxScroll - 2;
  };

  const move = (direction) => {
    viewport.scrollBy({ left: direction * viewport.clientWidth * 0.72, behavior: "smooth" });
  };

  previous?.addEventListener("click", () => move(-1));
  next?.addEventListener("click", () => move(1));
  viewport.addEventListener("scroll", updateArrows, { passive: true });
  window.addEventListener("resize", updateArrows);

  let dragging = false;
  let dragged = false;
  let startX = 0;
  let startScroll = 0;

  viewport.addEventListener("pointerdown", (event) => {
    if (event.pointerType !== "touch" && event.button !== 0) return;
    event.preventDefault();
    dragging = true;
    dragged = false;
    startX = event.clientX;
    startScroll = viewport.scrollLeft;
    viewport.classList.add("is-dragging");
    viewport.setPointerCapture(event.pointerId);
  });

  viewport.addEventListener("dragstart", (event) => event.preventDefault());

  viewport.addEventListener("pointermove", (event) => {
    if (!dragging) return;
    const distance = event.clientX - startX;
    if (Math.abs(distance) > 4) dragged = true;
    viewport.scrollLeft = startScroll - distance;
  });

  const stopDragging = (event) => {
    if (!dragging) return;
    dragging = false;
    viewport.classList.remove("is-dragging");
    if (viewport.hasPointerCapture(event.pointerId)) viewport.releasePointerCapture(event.pointerId);
  };

  viewport.addEventListener("pointerup", stopDragging);
  viewport.addEventListener("pointercancel", stopDragging);
  viewport.addEventListener("click", (event) => {
    if (dragged) {
      event.preventDefault();
      event.stopPropagation();
      dragged = false;
    }
  }, true);

  updateArrows();
});

const caseModal = document.querySelector("[data-case-modal]");
const caseContent = {
  "demo-one": {
    tag: "Метка кейса",
    title: "Заголовок первого кейса",
    lead: "Вводный рыба-текст показывает, как будет выглядеть краткое описание истории в модальном окне",
    image: "Демонстрационное изображение в пропорции 3:2",
    story: [
      ["Исходная ситуация", "Нейтральный текст описывает исходные условия и помогает оценить объём смыслового блока"],
      ["Последовательность действий", "Несколько предложений показывают структуру основной части истории и ритм чтения"],
      ["Итог", "Завершающий абзац демонстрирует место для результата, вывода или ключевого наблюдения"]
    ]
  },
  "demo-two": {
    tag: "Метка кейса",
    title: "Заголовок второго кейса",
    lead: "Другой вариант рыба-текста нужен для проверки карточек с разной длиной заголовка и описания",
    image: "Демонстрационное изображение в пропорции 3:2",
    story: [
      ["Контекст", "Первый фрагмент нейтрального текста задаёт контекст и показывает возможную плотность набора"],
      ["Основная часть", "Второй фрагмент занимает больше места и помогает проверить адаптивность модального окна"],
      ["Результат", "Короткая финальная формулировка завершает демонстрационную историю"]
    ]
  },
  repair: {
    tag: "Домовой сервис",
    title: "Неожиданно сломалась стиральная машина",
    lead: "Клиент обнаружил неисправность вечером и обратился в МСГ, чтобы понять причину поломки и дальнейшие действия",
    image: "Мастер диагностирует бытовую технику на месте",
    story: [
      ["Ситуация", "Стиральная машина остановилась во время работы и перестала запускать программу повторно"],
      ["Что сделали", "Оператор уточнил симптомы, проверил условия продукта и организовал обращение к профильному мастеру. Специалист провёл диагностику и определил неисправный узел"],
      ["Результат", "Клиент получил понятное заключение, рекомендации по ремонту и смог принять решение без самостоятельного поиска исполнителя"]
    ]
  },
  inspection: {
    tag: "Чекап квартиры",
    title: "Проверка жилья перед покупкой",
    lead: "Перед сделкой клиент хотел оценить техническое состояние квартиры и заранее увидеть возможные расходы",
    image: "Специалист осматривает квартиру перед покупкой",
    story: [
      ["Ситуация", "Квартира визуально выглядела готовой к проживанию, но у клиента оставались вопросы к электрике, сантехнике и качеству ремонта"],
      ["Что сделали", "Эксперт провёл осмотр основных систем, зафиксировал замечания и объяснил, какие из них требуют внимания в первую очередь"],
      ["Результат", "Клиент получил структурированный список наблюдений и использовал его при обсуждении условий покупки"]
    ]
  },
  plumbing: {
    tag: "Домовой сервис",
    title: "В квартире обнаружилась протечка",
    lead: "Клиент заметил воду под раковиной и обратился в МСГ, чтобы быстро определить источник проблемы",
    image: "Сантехник осматривает место протечки в квартире",
    story: [
      ["Ситуация", "Вода появлялась после использования раковины, но самостоятельно определить повреждённый участок не удалось"],
      ["Что сделали", "Оператор уточнил обстоятельства и организовал обращение к сантехнику. Специалист проверил соединения, обнаружил источник протечки и объяснил порядок работ"],
      ["Результат", "Клиент получил понятный план устранения неисправности и рекомендации по дальнейшей эксплуатации"]
    ]
  }
};

const openCaseModal = (key) => {
  const data = caseContent[key];
  if (!caseModal || !data) return;
  caseModal.querySelector("[data-case-tag]").textContent = data.tag;
  caseModal.querySelector("[data-case-title]").textContent = data.title;
  caseModal.querySelector("[data-case-lead]").textContent = data.lead;
  caseModal.querySelector("[data-case-image-text]").textContent = data.image;
  caseModal.querySelector("[data-case-story]").innerHTML = data.story
    .map(([title, text]) => `<p><strong>${title}</strong>${text}</p>`)
    .join("");
  caseModal.showModal();
};

document.querySelectorAll("[data-case-open]").forEach((card) => {
  card.addEventListener("click", () => openCaseModal(card.dataset.caseOpen));
  card.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" && event.key !== " ") return;
    event.preventDefault();
    openCaseModal(card.dataset.caseOpen);
  });
});

caseModal?.querySelector("[data-case-close]")?.addEventListener("click", () => caseModal.close());
caseModal?.querySelector("[data-case-consultation]")?.addEventListener("click", () => caseModal.close());
caseModal?.addEventListener("click", (event) => {
  if (event.target === caseModal) caseModal.close();
});

document.querySelectorAll("h1 + p, h2 + p, h3 + p").forEach((subtitle) => {
  subtitle.textContent = subtitle.textContent.replace(/\.\s*$/, "");
});

document.querySelectorAll("[data-demo-form]").forEach((form) => {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const button = form.querySelector("button[type='submit']");
    if (!button) return;
    const initial = button.textContent;
    button.textContent = "Заявка принята ✓";
    button.disabled = true;
    setTimeout(() => {
      button.textContent = initial;
      button.disabled = false;
      form.reset();
    }, 2600);
  });
});
