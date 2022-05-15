setInterval( function () {
        if (window.innerHeight + window.pageYOffset >= document.body.scrollHeight) {
            window.scrollTo({top: 0, behavior: 'smooth'});
            localStorage.setItem('scroll', 'true');
            setTimeout(function () {localStorage.setItem('scroll', 'false')}, 3000);
        } else if (localStorage.getItem('scroll') == 'false') {
            window.scrollBy(0, 1);
//            console.log("HELLO???");
        }
    }, 20);