function excerpt() {
    const excerpt = document.querySelector("#excerpt");
    if (excerpt) {
        Array.from(excerpt.children).forEach(n => {
            if (n.innerHTML === "&nbsp;") {
                n.remove()
            };
        const allowedNode = ["h1", "h2", "h3", "h4", "h5", "h6", "p"]
        const contain = allowedNode.includes(n.localName);
            Array.from(n.childNodes).find(n => {
                if (n.localName === "img") {
                    n.parentNode.remove();
                }
            });
        if (!contain) n.remove();
        })
    }
}

excerpt();