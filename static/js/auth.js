document.addEventListener("DOMContentLoaded", () => {
    const tabButtons = document.querySelectorAll(".tab-button");
    const sectionNames = ["login", "register", "forgot", "verify", "reset"];
    const sections = sectionNames
        .map((name) => document.getElementById(`${name}-section`))
        .filter(Boolean);

    if (!sections.length) {
        return;
    }

    function setActiveTab(tab) {
        tabButtons.forEach((button) => {
            button.classList.toggle("active", button.dataset.target === tab);
        });

        sections.forEach((section) => {
            section.classList.toggle("active", section.id === `${tab}-section`);
        });
    }

    tabButtons.forEach((button) => {
        button.addEventListener("click", () => setActiveTab(button.dataset.target));
    });

    setActiveTab(window.selectedTab || "login");
});