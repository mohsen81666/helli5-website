function copy_to_clipboard() {
    /* Get the text field */
    var copyText = document.getElementById("url_to_copy");

    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /*For mobile devices*/

    /* Copy the text inside the text field */
    document.execCommand("copy");

    /* Alert the copied text */
    alert("از طریق آدرس کپی شده می توانید اطلاعات خود را ویرایش کنید");
}

$(document).ready(function () {

    $('#id_student_picture').bind('change', function (event) {
        if (this.files[0].size > 500000) {
            this.val(null);
            alert('حجم فایل بیش از حد مجاز است');
        }

    });
    $("#id_melli_code #id_ss_id, #id_ss_numerical, #id_father_job_phone, #id_mother_job_phone, #id_home_phone, #id_father_phone, #id_mother_phone, #id_student_phone").on("keypress keyup blur", function (event) {
        $(this).val($(this).val().replace(/[^\d].+/, ""));
        if ((event.which < 48 || event.which > 57)) {
            event.preventDefault();
        }
    });
    $("id_grade_at_9th").on("keypress keyup blur", function (event) {
        $(this).val($(this).val().replace(/[^0-9\.]/g, ''));
        if ((event.which != 46 || $(this).val().indexOf('.') != -1) && (event.which < 48 || event.which > 57)) {
            event.preventDefault();
        }
    });


    let error_list = [];

    $("#pre_registeration-save").click(function (event) {
        let browser_check_validition = document.forms["pre_registeration"].reportValidity();
        if(browser_check_validition) {
            let student_shenasname_seri = $("#id_ss_id");
            let melli_code = $("#id_melli_code");
            let father_job_place = $("#id_father_job_place");
            let home_location = $("#id_home_location");
            let home_phone = $("#id_home_phone");
            let home_postal = $("#id_home_postal_code");
            let father_phone = $("#id_father_phone");
            let mother_phone = $("#id_mother_phone");
            let this_child_counter = $("#id_this_child_counter");
            let family_children_counter = $("#id_family_children_counter");
            let student_mail = $("#id_student_mail");
            let student_phone = $("#id_student_phone");
            let field_of_study = $("#id_field_of_study");
            let grade_at_9th = $("#id_grade_at_9th");

            if (melli_code.val() === undefined || !validateMelliCode(melli_code.val())) {
                error("کد ملی نا معتبر است.");
            }
            if (student_shenasname_seri.val() === undefined || student_shenasname_seri.val().length !== 6) {
                error("سریال ۶ رقمی شناسنامه نا معتبر است.");
            }
            if (father_job_place.val() === undefined || father_job_place.val().length < 10) {
                error("محل کار  پدر نا معتبر است.");
            }
            if (home_location.val() === undefined || home_location.val().length < 10) {
                error("آدرس منزل نا معتبر است.");
            }
            if (home_postal.val() === undefined || home_postal.val().length < 10) {
                error("کدپستی نا معتبر است.");
            }
            if (home_phone.val() === undefined && home_phone.val().length < 8) {
                error("شماره منزل نا معتبر است.");
            }
            if (father_phone.val() === undefined || father_phone.val().length != 11) {
                error("شماره موبایل پدر نا معتبر است.");
            }
            if (mother_phone.val() === undefined || mother_phone.val().length != 11) {
                error("شماره موبایل مادر نا معتبر است.");
            }
            if (this_child_counter.val() === undefined || parseInt(this_child_counter.val()) < 1) {
                error("چندمین فرزند است  نا معتبر است.");
            }
            if (family_children_counter.val() === undefined || parseInt(family_children_counter.val()) < 1) {
                error("تعداد فرزندان خانواده نا معتبر است.");
            }
            if (student_mail.val() !== undefined && student_mail.val() !== '' && !isEmail(student_mail.val())) {
                error("ایمیل دانش آموز  نا معتبر است.");
            }
            if (student_phone.val() === undefined || student_phone.val().length !== 11) {
                error("شماره موبایل دانش آموز نا معتبر است.");
            }
            if (field_of_study.val() === undefined || field_of_study.val().length === 0) {
                error("رشته مورد علاقه نا معتبر است.");
            }
            if (grade_at_9th.val() === undefined || parseFloat(grade_at_9th.val()) < 0 || parseFloat(grade_at_9th.val()) > 20) {
                error("معدل کل  نا معتبر است.");
            }

            if (error_list.length === 0)
                $("#pre_registeration").submit();
            else {
                event.preventDefault();
                show_error_list();
            }
        }
    });

    function error(message) {
        error_list[error_list.length] = message;
    }

    $(window).keydown(function (event) {
        if (event.keyCode == 13) {
            event.preventDefault();
            return false;
        }
    });

    function show_error_list() {
        $("#error-container").empty();

        let error_element = "";
        error_list.forEach(function (item) {
            error_element += "<div dir='rtl' class='alert alert-danger text-right'><strong>" + item + "  </strong></div>\n";
        })
        $("#error-container").append(error_element);
        error_list = [];
    }
});

function validateMelliCode(melliCode) {
    if (melliCode.length !== 10) {
        return false; // Melli Code is less or more than 10 digits

    } else {
        let sum = 0;
        for (let i = 0; i < 9; i++) {
            sum += parseInt(melliCode.charAt(i)) * (10 - i);
        }

        let lastDigit;
        let divideRemaining = sum % 11;
        if (divideRemaining < 2) {
            lastDigit = divideRemaining;
        } else {
            lastDigit = 11 - (divideRemaining);
        }

        if (parseInt(melliCode.charAt(9)) === lastDigit) {
            return true;
        } else {
            return false; // Invalid MelliCode
        }
    }
}

function isEmail(email) {
    let regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if (!regex.test(email)) {
        return false;
    } else {
        return true;
    }
}