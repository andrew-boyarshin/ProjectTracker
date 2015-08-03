var doughnutData = [
    {
        value: right_percent,
        color:"#4CAF50",
        highlight: "#66BB6A",
        label: "Right(%)"
    },
    {
        value: wrong_percent,
        color: "#F44336",
        highlight: "#EF5350",
        label: "Wrong(%)"
    }
];
window.onload = function(){
    var ctx = document.getElementById("chart-area").getContext("2d");
    window.myDoughnut = new Chart(ctx).Doughnut(doughnutData, {responsive : true});
};