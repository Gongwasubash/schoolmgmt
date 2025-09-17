// Chart.js implementation for dashboard charts
document.addEventListener('DOMContentLoaded', function() {
    // Student Distribution Chart
    const studentCtx = document.getElementById('studentChart');
    if (studentCtx) {
        const chart = new Chart(studentCtx, {
            type: 'doughnut',
            data: {
                labels: ['Nursery', 'KG', 'Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5', 'Class 6', 'Class 7', 'Class 8', 'Class 9', 'Class 10'],
                datasets: [{
                    data: [25, 22, 18, 16, 15, 14, 13, 12, 11, 10, 9, 8],
                    backgroundColor: [
                        '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', 
                        '#06b6d4', '#84cc16', '#f97316', '#ec4899', '#6366f1',
                        '#14b8a6', '#f43f5e'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '60%',
                animation: {
                    animateRotate: true,
                    animateScale: true,
                    duration: 1000
                },
                hover: {
                    animationDuration: 300
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'right',
                        labels: {
                            fontSize: 10,
                            padding: 8,
                            usePointStyle: true
                        }
                    }
                },
                onClick: (event, elements) => {
                    if (elements.length > 0) {
                        const index = elements[0].index;
                        const label = chart.data.labels[index];
                        const value = chart.data.datasets[0].data[index];
                        
                        const centerDiv = document.querySelector('.chart-center');
                        centerDiv.querySelector('.center-label').textContent = label;
                        centerDiv.querySelector('.center-value').textContent = value;
                    }
                }
            }
        });
    }

    // Gender Chart
    const genderCtx = document.getElementById('genderChart');
    if (genderCtx) {
        new Chart(genderCtx, {
            type: 'doughnut',
            data: {
                labels: ['Boys', 'Girls'],
                datasets: [{
                    data: [169, 21],
                    backgroundColor: ['#3b82f6', '#ec4899'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '60%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            fontSize: 12,
                            padding: 10
                        }
                    }
                }
            }
        });
    }

    // Religion Chart
    const religionCtx = document.getElementById('religionChart');
    if (religionCtx) {
        new Chart(religionCtx, {
            type: 'doughnut',
            data: {
                labels: ['Hindu', 'Muslim', 'Christian', 'Others'],
                datasets: [{
                    data: [120, 45, 20, 5],
                    backgroundColor: ['#f59e0b', '#10b981', '#8b5cf6', '#6b7280'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '60%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            fontSize: 12,
                            padding: 10
                        }
                    }
                }
            }
        });
    }

    // Category Chart
    const categoryCtx = document.getElementById('categoryChart');
    if (categoryCtx) {
        new Chart(categoryCtx, {
            type: 'doughnut',
            data: {
                labels: ['General', 'OBC', 'SC', 'ST'],
                datasets: [{
                    data: [95, 60, 25, 10],
                    backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '60%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            fontSize: 12,
                            padding: 10
                        }
                    }
                }
            }
        });
    }
});