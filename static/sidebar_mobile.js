
const sidebarWidth = $(":root").css("--sidebarwidth")
console.log("sidebarWidth = ", sidebarWidth)

function openNav() {
    $("#leftSidebar").css("width", sidebarWidth);
    $("#leftSidebar").css("left", "0");
}
/* Set the width of the sidebar to 0
and the left margin of the page content to 0 */
function closeNav() {
    console.log("close")
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

    lastExecMouseMove = Date.now()
    if (parseInt(e.clientX) >= parseInt(sidebarWidth)) {

        closeNav()


    }

})
