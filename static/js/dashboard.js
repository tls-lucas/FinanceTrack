document.addEventListener("DOMContentLoaded", () => {
    const periodSelect = document.getElementById("dashboard-period");
    const monthControl = document.getElementById("month-control");
    const yearControl = document.getElementById("year-control");

    if (periodSelect && monthControl && yearControl) {
        const updateFilterVisibility = () => {
            const value = periodSelect.value;
            monthControl.style.display = value === "month" ? "grid" : "none";
            yearControl.style.display = value === "year" ? "grid" : "none";
        };

        periodSelect.addEventListener("change", updateFilterVisibility);
        updateFilterVisibility();
    }

    if (document.getElementById("lineChart")) {
        const lineCtx = document.getElementById("lineChart").getContext("2d");
        const data = window.dashboardChartData || {
            labels: ["01", "05", "10", "15", "20", "25", "30"],
            incomes: [900, 2500, 3400, 4200, 5300, 6700, 7400],
            expenses: [300, 1200, 2700, 3500, 4300, 5100, 4980],
            balances: [600, 1300, 1300, 1300, 1000, 1600, 2440],
        };

        const isGeneral = window.dashboardPeriod === "all";
        const chartConfig = {
            type: isGeneral ? "bar" : "line",
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: "Receitas",
                        data: data.incomes,
                        borderColor: "#1c9a41",
                        backgroundColor: isGeneral ? "rgba(28, 154, 65, 0.8)" : "rgba(28, 154, 65, 0.08)",
                        fill: !isGeneral,
                        tension: 0.35,
                        pointRadius: 0,
                    },
                    {
                        label: "Despesas",
                        data: data.expenses.map((value) => -value),
                        borderColor: "#d63447",
                        backgroundColor: isGeneral ? "rgba(214, 52, 71, 0.8)" : "rgba(214, 52, 71, 0.08)",
                        fill: !isGeneral,
                        tension: 0.35,
                        pointRadius: 0,
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true, position: "bottom" },
                },
                scales: {
                    x: { grid: { display: false } },
                    y: { grid: { color: "rgba(15, 33, 72, 0.08)" }, ticks: { beginAtZero: true } },
                },
            },
        };

        if (!isGeneral) {
            chartConfig.data.datasets.push({
                label: "Saldo Acumulado",
                data: data.balances,
                borderColor: "#fb923c",
                borderDash: [8, 6],
                backgroundColor: "rgba(251, 146, 60, 0.08)",
                fill: false,
                tension: 0.35,
                pointRadius: 0,
            });
        } else {
            chartConfig.options.scales.x.barPercentage = 0.6;
            chartConfig.options.scales.x.categoryPercentage = 0.7;
        }

        new Chart(lineCtx, chartConfig);
    }

    if (document.getElementById("donutChart")) {
        const donutCtx = document.getElementById("donutChart").getContext("2d");
        const data = window.dashboardChartData || {
            category_labels: ["Moradia", "Alimentação", "Educação", "Transporte", "Outros"],
            category_values: [30, 25, 10, 10, 25],
        };

        new Chart(donutCtx, {
            type: "doughnut",
            data: {
                labels: data.category_labels,
                datasets: [{
                    data: data.category_values,
                    backgroundColor: ["#1d4ed8", "#f59e0b", "#ef4444", "#2dd4bf", "#16a34a"],
                    borderWidth: 0,
                }],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                },
                cutout: "72%",
            },
        });
    }
});