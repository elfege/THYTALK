
const sidebarWidth = $(":root").css("--sidebarwidth")
console.log("sidebarWidth = ", sidebarWidth)

function openNav() {
    $("#leftSidebar").css("width", sidebarWidth);
    $("#leftSidebar").css("left", "0");
    // $("#mainContent").parent().prepend("<div class='col-xs-4' id='addedLeftCol'>")
    // $("#mainContent").removeClass();
    // $("#mainContent").addClass("col-xs-8");
}
/* Set the width of the sidebar to 0
and the left margin of the page content to 0 */
function closeNav() {
    console.log("close")
    // $("#addedLeftCol").remove()
    // $("#mainContent").removeClass();
    // $("#mainContent").addClass("col-xs-12");
    $("#leftSidebar").css("width", "0");
    setTimeout(fullHide, 600)

}
$(document).ready(() => closeNav())

function fullHide() {
    $("#leftSidebar").css("left", "-1020px");
}

$("#savedArticlesSubmenu_mobile_btn").click(() => {
    console.log("click")
    openNav()
})

let lastExecMouseMove = Date.now()
$("body").on("click", (e) => {

    // navState = $(".sidenav").css("width") === "0px" ? "closed" : "open"
    // console.log("openNavFired:", openNavFired)
    // console.log("closeNavFired:", closeNavFired)
    // if (Date.now() - lastExecMouseMove >= 1000) {
    lastExecMouseMove = Date.now()
    if (parseInt(e.clientX) >= parseInt(sidebarWidth)) {

        closeNav()


    }

})
