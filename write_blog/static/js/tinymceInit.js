tinymce.init({
    selector: 'textarea#id_body',
    skin: "CUSTOM",
    height: 600,
    menubar: false,
    plugins: 'print preview paste autolink autosave save directionality code visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak anchor advlist lists wordcount imagetools noneditable charmap quickbars',
    toolbar: 'formatselect| bold italic underline strikethrough table | alignleft aligncenter alignright alignjustify |  numlist bullist | fullscreen  preview | insertfile image media link anchor codesample',
    images_upload_url: '/',
});
