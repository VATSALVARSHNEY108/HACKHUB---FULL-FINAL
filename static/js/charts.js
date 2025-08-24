// HackHub Charts - Data Visualization with Chart.js

// Global chart configuration
Chart.defaults.color = '#a0a0a0';
Chart.defaults.backgroundColor = 'rgba(102, 126, 234, 0.2)';
Chart.defaults.borderColor = 'rgba(102, 126, 234, 0.8)';
Chart.defaults.plugins.legend.labels.usePointStyle = true;

// Color palette for charts
const chartColors = {
    primary: '#667eea',
    secondary: '#f093fb',
    success: '#43e97b',
    info: '#4facfe',
    warning: '#ffc107',
    danger: '#f5576c',
    light: '#f8f9fa',
    dark: '#343a40'
};

const gradientColors = [
    'rgba(102, 126, 234, 0.8)',
    'rgba(240, 147, 251, 0.8)',
    'rgba(67, 233, 123, 0.8)',
    'rgba(79, 172, 254, 0.8)',
    'rgba(255, 193, 7, 0.8)',
    'rgba(245, 87, 108, 0.8)',
    'rgba(108, 117, 125, 0.8)',
    'rgba(52, 58, 64, 0.8)'
];

// Chart utility functions
function createGradient(ctx, color1, color2) {
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, color1);
    gradient.addColorStop(1, color2);
    return gradient;
}

function getResponsiveOptions(maintainAspectRatio = true) {
    return {
        responsive: true,
        maintainAspectRatio: maintainAspectRatio,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    padding: 20,
                    usePointStyle: true,
                    font: {
                        size: 12,
                        family: 'Inter, sans-serif'
                    }
                }
            },
            tooltip: {
                backgroundColor: 'rgba(22, 33, 62, 0.95)',
                titleColor: '#ffffff',
                bodyColor: '#a0a0a0',
                borderColor: 'rgba(102, 126, 234, 0.3)',
                borderWidth: 1,
                cornerRadius: 8,
                displayColors: true,
                titleFont: {
                    size: 14,
                    weight: 'bold'
                },
                bodyFont: {
                    size: 12
                }
            }
        },
        scales: {
            x: {
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)',
                    drawBorder: false
                },
                ticks: {
                    color: '#a0a0a0',
                    font: {
                        size: 11
                    }
                }
            },
            y: {
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)',
                    drawBorder: false
                },
                ticks: {
                    color: '#a0a0a0',
                    font: {
                        size: 11
                    }
                }
            }
        }
    };
}

// Dashboard Charts
async function loadDashboardCharts() {
    try {
        const response = await fetch('/api/team-stats');
        const data = await response.json();

        if (data.success === false) {
            console.error('Failed to load team stats:', data.message);
            return;
        }

        createRoleDistributionChart(data.role_distribution);
        createExperienceDistributionChart(data.experience_distribution);
    } catch (error) {
        console.error('Error loading dashboard charts:', error);
        // Create empty charts with placeholder data
        createRoleDistributionChart({});
        createExperienceDistributionChart({});
    }
}

function createRoleDistributionChart(roleData) {
    const ctx = document.getElementById('roleChart');
    if (!ctx) return;

    const hasData = Object.keys(roleData).length > 0;
    const labels = hasData ? Object.keys(roleData) : ['No Data'];
    const values = hasData ? Object.values(roleData) : [1];
    const colors = hasData ? gradientColors.slice(0, labels.length) : ['rgba(108, 117, 125, 0.5)'];

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors,
                borderColor: colors.map(color => color.replace('0.8', '1')),
                borderWidth: 2,
                hoverBackgroundColor: colors.map(color => color.replace('0.8', '0.9')),
                hoverBorderWidth: 3
            }]
        },
        options: {
            ...getResponsiveOptions(false),
            cutout: '60%',
            plugins: {
                ...getResponsiveOptions().plugins,
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        generateLabels: function(chart) {
                            const data = chart.data;
                            if (data.labels.length && data.datasets.length) {
                                return data.labels.map((label, i) => {
                                    const dataset = data.datasets[0];
                                    const value = dataset.data[i];
                                    const total = dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = total > 0 ? Math.round((value / total) * 100) : 0;

                                    return {
                                        text: `${label} (${percentage}%)`,
                                        fillStyle: dataset.backgroundColor[i],
                                        strokeStyle: dataset.borderColor[i],
                                        lineWidth: dataset.borderWidth,
                                        pointStyle: 'circle',
                                        hidden: false,
                                        index: i
                                    };
                                });
                            }
                            return [];
                        }
                    }
                },
                tooltip: {
                    ...getResponsiveOptions().plugins.tooltip,
                    callbacks: {
                        label: function(context) {
                            if (!hasData) return 'No participants registered yet';

                            const label = context.label || '';
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            },
            animation: {
                animateRotate: true,
                animateScale: true,
                duration: 1000,
                easing: 'easeInOutQuart'
            }
        }
    });
}

function createExperienceDistributionChart(experienceData) {
    const ctx = document.getElementById('experienceChart');
    if (!ctx) return;

    const hasData = Object.keys(experienceData).length > 0;
    const labels = hasData ? Object.keys(experienceData) : ['No Data'];
    const values = hasData ? Object.values(experienceData) : [1];

    // Create gradient backgrounds
    const gradient1 = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
    gradient1.addColorStop(0, 'rgba(67, 233, 123, 0.8)');
    gradient1.addColorStop(1, 'rgba(67, 233, 123, 0.2)');

    const gradient2 = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
    gradient2.addColorStop(0, 'rgba(79, 172, 254, 0.8)');
    gradient2.addColorStop(1, 'rgba(79, 172, 254, 0.2)');

    const gradient3 = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
    gradient3.addColorStop(0, 'rgba(240, 147, 251, 0.8)');
    gradient3.addColorStop(1, 'rgba(240, 147, 251, 0.2)');

    const backgrounds = hasData ? [gradient1, gradient2, gradient3] : ['rgba(108, 117, 125, 0.5)'];
    const borderColors = hasData ? [
        'rgba(67, 233, 123, 1)',
        'rgba(79, 172, 254, 1)',
        'rgba(240, 147, 251, 1)'
    ] : ['rgba(108, 117, 125, 1)'];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: hasData ? 'Participants' : 'No Data',
                data: values,
                backgroundColor: backgrounds.slice(0, labels.length),
                borderColor: borderColors.slice(0, labels.length),
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false,
                hoverBackgroundColor: backgrounds.slice(0, labels.length).map(bg =>
                    typeof bg === 'string' ? bg.replace('0.5', '0.7') : bg
                ),
                hoverBorderWidth: 3
            }]
        },
        options: {
            ...getResponsiveOptions(false),
            scales: {
                x: {
                    ...getResponsiveOptions().scales.x,
                    grid: {
                        display: false
                    }
                },
                y: {
                    ...getResponsiveOptions().scales.y,
                    beginAtZero: true,
                    ticks: {
                        ...getResponsiveOptions().scales.y.ticks,
                        stepSize: 1,
                        callback: function(value) {
                            return Number.isInteger(value) ? value : '';
                        }
                    }
                }
            },
            plugins: {
                ...getResponsiveOptions().plugins,
                legend: {
                    display: false
                },
                tooltip: {
                    ...getResponsiveOptions().plugins.tooltip,
                    callbacks: {
                        title: function(context) {
                            return `Experience Level: ${context[0].label}`;
                        },
                        label: function(context) {
                            if (!hasData) return 'No participants registered yet';

                            const value = context.parsed.y;
                            return `${value} participant${value !== 1 ? 's' : ''}`;
                        }
                    }
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeInOutQuart',
                delay: function(context) {
                    return context.dataIndex * 100;
                }
            }
        }
    });
}

// Team Analytics Charts
function createTeamSizeChart(teamSizes) {
    const ctx = document.getElementById('teamSizeChart');
    if (!ctx) return;

    const hasData = teamSizes && teamSizes.length > 0;

    if (!hasData) {
        // Show empty state
        ctx.getContext('2d').fillStyle = '#6c757d';
        ctx.getContext('2d').textAlign = 'center';
        ctx.getContext('2d').font = '16px Inter';
        ctx.getContext('2d').fillText('No teams created yet', ctx.width / 2, ctx.height / 2);
        return;
    }

    // Calculate size distribution
    const sizeDistribution = {};
    teamSizes.forEach(size => {
        sizeDistribution[size] = (sizeDistribution[size] || 0) + 1;
    });

    const labels = Object.keys(sizeDistribution).map(size => `${size} member${size !== '1' ? 's' : ''}`);
    const values = Object.values(sizeDistribution);

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: gradientColors.slice(0, labels.length),
                borderColor: gradientColors.slice(0, labels.length).map(color => color.replace('0.8', '1')),
                borderWidth: 2,
                hoverBackgroundColor: gradientColors.slice(0, labels.length).map(color => color.replace('0.8', '0.9')),
                hoverBorderWidth: 3
            }]
        },
        options: {
            ...getResponsiveOptions(false),
            cutout: '50%',
            plugins: {
                ...getResponsiveOptions().plugins,
                tooltip: {
                    ...getResponsiveOptions().plugins.tooltip,
                    callbacks: {
                        label: function(context) {
                            const label = context.label;
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ${value} team${value !== 1 ? 's' : ''} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

function createBalanceScoreChart(balanceScores) {
    const ctx = document.getElementById('balanceScoreChart');
    if (!ctx) return;

    const hasData = balanceScores && balanceScores.length > 0;

    if (!hasData) {
        // Show empty state
        ctx.getContext('2d').fillStyle = '#6c757d';
        ctx.getContext('2d').textAlign = 'center';
        ctx.getContext('2d').font = '16px Inter';
        ctx.getContext('2d').fillText('No teams created yet', ctx.width / 2, ctx.height / 2);
        return;
    }

    const labels = balanceScores.map((_, index) => `Team ${index + 1}`);

    // Create gradient background
    const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(79, 172, 254, 0.8)');
    gradient.addColorStop(1, 'rgba(79, 172, 254, 0.2)');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Balance Score',
                data: balanceScores,
                backgroundColor: gradient,
                borderColor: '#4facfe',
                borderWidth: 2,
                borderRadius: 6,
                borderSkipped: false,
                hoverBackgroundColor: 'rgba(79, 172, 254, 0.9)',
                hoverBorderWidth: 3
            }]
        },
        options: {
            ...getResponsiveOptions(false),
            scales: {
                x: {
                    ...getResponsiveOptions().scales.x,
                    grid: {
                        display: false
                    }
                },
                y: {
                    ...getResponsiveOptions().scales.y,
                    beginAtZero: true,
                    max: 1.0,
                    ticks: {
                        ...getResponsiveOptions().scales.y.ticks,
                        callback: function(value) {
                            return value.toFixed(1);
                        }
                    }
                }
            },
            plugins: {
                ...getResponsiveOptions().plugins,
                legend: {
                    display: false
                },
                tooltip: {
                    ...getResponsiveOptions().plugins.tooltip,
                    callbacks: {
                        title: function(context) {
                            return context[0].label;
                        },
                        label: function(context) {
                            const score = context.parsed.y;
                            let rating = '';
                            if (score >= 0.8) rating = 'Excellent';
                            else if (score >= 0.6) rating = 'Good';
                            else if (score >= 0.4) rating = 'Fair';
                            else rating = 'Needs Improvement';

                            return `Balance Score: ${score.toFixed(3)} (${rating})`;
                        }
                    }
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeInOutQuart',
                delay: function(context) {
                    return context.dataIndex * 100;
                }
            }
        }
    });
}

// Skills Distribution Chart
function createSkillsDistributionChart(skillsData) {
    const ctx = document.getElementById('skillsChart');
    if (!ctx) return;

    const hasData = skillsData && Object.keys(skillsData).length > 0;

    if (!hasData) {
        return;
    }

    // Get top 10 skills
    const sortedSkills = Object.entries(skillsData)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 10);

    const labels = sortedSkills.map(([skill]) => skill);
    const values = sortedSkills.map(([, count]) => count);

    // Create gradient background
    const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(102, 126, 234, 0.8)');
    gradient.addColorStop(1, 'rgba(102, 126, 234, 0.2)');

    new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Skill Count',
                data: values,
                backgroundColor: gradient,
                borderColor: '#667eea',
                borderWidth: 2,
                borderRadius: 6,
                borderSkipped: false
            }]
        },
        options: {
            ...getResponsiveOptions(false),
            indexAxis: 'y',
            scales: {
                x: {
                    ...getResponsiveOptions().scales.x,
                    beginAtZero: true,
                    ticks: {
                        ...getResponsiveOptions().scales.x.ticks,
                        stepSize: 1
                    }
                },
                y: {
                    ...getResponsiveOptions().scales.y,
                    grid: {
                        display: false
                    }
                }
            },
            plugins: {
                ...getResponsiveOptions().plugins,
                legend: {
                    display: false
                }
            }
        }
    });
}

// Hackathon Timeline Chart
function createHackathonTimelineChart(hackathonData) {
    const ctx = document.getElementById('hackathonTimelineChart');
    if (!ctx) return;

    const hasData = hackathonData && hackathonData.length > 0;

    if (!hasData) {
        return;
    }

    // Sort hackathons by date
    const sortedHackathons = hackathonData
        .filter(h => h.start_date)
        .sort((a, b) => new Date(a.start_date) - new Date(b.start_date));

    const labels = sortedHackathons.map(h => {
        const date = new Date(h.start_date);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });

    const teamCounts = sortedHackathons.map(h => h.team_count || 0);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Teams Registered',
                data: teamCounts,
                borderColor: '#43e97b',
                backgroundColor: 'rgba(67, 233, 123, 0.1)',
                borderWidth: 3,
                pointBackgroundColor: '#43e97b',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            ...getResponsiveOptions(false),
            scales: {
                x: {
                    ...getResponsiveOptions().scales.x,
                    grid: {
                        display: false
                    }
                },
                y: {
                    ...getResponsiveOptions().scales.y,
                    beginAtZero: true,
                    ticks: {
                        ...getResponsiveOptions().scales.y.ticks,
                        stepSize: 1
                    }
                }
            },
            plugins: {
                ...getResponsiveOptions().plugins,
                legend: {
                    display: false
                }
            }
        }
    });
}

// Chart update functions
function updateChart(chartId, newData) {
    const canvas = document.getElementById(chartId);
    if (!canvas) return;

    const chart = Chart.getChart(canvas);
    if (chart) {
        chart.data = newData;
        chart.update('active');
    }
}

function destroyChart(chartId) {
    const canvas = document.getElementById(chartId);
    if (!canvas) return;

    const chart = Chart.getChart(canvas);
    if (chart) {
        chart.destroy();
    }
}

// Real-time chart updates
function setupRealTimeCharts() {
    // Check for data updates every 30 seconds
    setInterval(async () => {
        try {
            const response = await fetch('/api/team-stats');
            const data = await response.json();

            if (data.success !== false) {
                // Update existing charts with new data
                const roleChart = Chart.getChart('roleChart');
                const experienceChart = Chart.getChart('experienceChart');

                if (roleChart && Object.keys(data.role_distribution).length > 0) {
                    roleChart.data.labels = Object.keys(data.role_distribution);
                    roleChart.data.datasets[0].data = Object.values(data.role_distribution);
                    roleChart.update('none');
                }

                if (experienceChart && Object.keys(data.experience_distribution).length > 0) {
                    experienceChart.data.labels = Object.keys(data.experience_distribution);
                    experienceChart.data.datasets[0].data = Object.values(data.experience_distribution);
                    experienceChart.update('none');
                }
            }
        } catch (error) {
            console.error('Error updating charts:', error);
        }
    }, 30000);
}

// Export chart as image
function exportChart(chartId, filename = 'chart') {
    const canvas = document.getElementById(chartId);
    if (!canvas) return;

    const chart = Chart.getChart(canvas);
    if (chart) {
        const link = document.createElement('a');
        link.download = `${filename}.png`;
        link.href = canvas.toDataURL('image/png');
        link.click();
    }
}

// Initialize charts when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Setup real-time updates if on dashboard
    if (window.location.pathname === '/' || window.location.pathname === '/index') {
        setupRealTimeCharts();
    }
});

// Global chart functions
window.HackHubCharts = {
    loadDashboardCharts,
    createTeamSizeChart,
    createBalanceScoreChart,
    createSkillsDistributionChart,
    createHackathonTimelineChart,
    updateChart,
    destroyChart,
    exportChart
};
