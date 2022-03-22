class JsAccordion {

    constructor(accordion_id, collapse = false, animation_class_list = []) {
        this.accordion = accordion_id;
        this.collapse = collapse;
        this.animationClassList = animation_class_list;
        this.menu_headers = this.accordion.querySelectorAll(".accordion-header");
        for (var k = 0; k < this.menu_headers.length; k++) {
            this.menu_headers[k].onclick = this.toggleAccordion.bind(this);
        }
    }

    toggleAccordion(event) {
        var header = event.target;
        var content_id = header.nextElementSibling;
        if (this.collapse && header.classList.contains("active-accordion")) {
            this.removeActiveHeadClass();
            content_id.style.display = "none";
            content_id.classList.remove(...this.animationClassList);
        } else {
            let tabs_panel = this.accordion.querySelectorAll(".accordion-content");
            for (let k = 0; k < tabs_panel.length; k++) {
                tabs_panel[k].style.display = "none";
                tabs_panel[k].classList.remove(...this.animationClassList);
            }
            this.removeActiveHeadClass();
            header.classList.add("active-accordion");
            content_id.classList.add(...this.animationClassList);
            content_id.style.display = "block";
        }
        event.preventDefault();
    }
    
    removeActiveHeadClass() {
        for (let i = 0; i < this.menu_headers.length; i++) {
            this.menu_headers[i].classList.remove("active-accordion");
        }
    }
}