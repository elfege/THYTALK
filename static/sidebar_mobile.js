
const sidebarWidth = $(":root").css("--sidebarwidth")
console.log("sidebarWidth = ", sidebarWidth)

function openNav() {
    $("#mySidebar").css("width", sidebarWidth);
    $("#mySidebar").css("left", "0");
    // $("#mySidebar").show()
}
/* Set the width of the sidebar to 0
and the left margin of the page content to 0 */
function closeNav() {
    $("#mySidebar").css("width", "0");
    setTimeout(fullHide, 600)
    // $("#mySidebar").hide()
}
$(document).ready(() => closeNav())

function fullHide() {
    $("#mySidebar").css("left", "-1020px");
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
