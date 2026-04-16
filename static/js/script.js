document.addEventListener('DOMContentLoaded', function () {

    // === CONFIGURACIÓN SELECT2 GENERAL ===
    $('.select2').select2({
        theme: 'bootstrap-5',
        placeholder: "---------",
        width: '100%',
        allowClear: true,
        language: "es"
    });

    // === FUNCIONES DE TOGGLE CAMPOS ===
    function toggleCampos(triggerName, targetId, expectedValue = 'True') {
        const radios = document.getElementsByName(triggerName);
        const target = document.getElementById(targetId);

        radios.forEach(radio => {
            radio.addEventListener('change', function () {
                target.classList.toggle('d-none', !(radio.checked && radio.value === expectedValue));
            });

            if (radio.checked && radio.value === expectedValue) {
                target.classList.remove('d-none');
            }
        });
    }

    toggleCampos('sexo', 'embarazoCampos', 'True');
    toggleCampos('embarazo', 'semanasEmbarazo', '2');
    toggleCampos('fuma', 'fumaCampos');
    toggleCampos('toma', 'tomaCampos');
    toggleCampos('testElisa', 'testElisaCampos');
    toggleCampos('cirugia', 'cirugiaCampos');
    toggleCampos('transfucion', 'transfucionCampos');

    // === PLAN TRATAMIENTO FORMSET ===
    const planContainer = document.getElementById("procedimientos-container-plan");
    const totalFormsPlan = document.getElementById("id_plantratamiento_procedimiento_set-TOTAL_FORMS");
    const emptyFormPlanDiv = document.getElementById("empty-form-plan");

    if (!planContainer) console.error("No se encontró el div procedimientos-container-plan");
    if (!totalFormsPlan) console.error("No se encontró el input id_plantratamiento_procedimiento_set-TOTAL_FORMS");
    if (!emptyFormPlanDiv) console.error("No se encontró el div empty-form-plan");

    const emptyFormPlan = emptyFormPlanDiv ? emptyFormPlanDiv.innerHTML : null;

    window.addPlanForm = function () {
        if (!emptyFormPlan) {
            console.error("No se puede añadir el form porque emptyFormPlan es null");
            return;
        }

        let formIndex = parseInt(totalFormsPlan.value);
        const newFormHtml = emptyFormPlan.replace(/__prefix__/g, formIndex);

        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = newFormHtml;

        tempDiv.querySelectorAll("input, select, textarea").forEach(el => {
            if (el.type === "checkbox") el.checked = false;
            else el.value = "";
        });

        tempDiv.querySelectorAll('span.select2').forEach(el => el.remove());

        tempDiv.querySelectorAll("input, select, textarea").forEach(el => {
            if (el.type === "checkbox") el.checked = false;
            else el.value = "";
        });

        const newForm = tempDiv.firstElementChild;
        planContainer.appendChild(newForm);

        $(newForm).find(".select2").select2({
            width: '100%',
            theme: 'bootstrap-5',
            dropdownParent: $('#procedimientos-container-plan')
        });

        totalFormsPlan.value = formIndex + 1;
    };

    window.removePlanForm = function (btn) {
        const formDiv = btn.closest(".formset-form");
        if (formDiv) formDiv.remove();
    };

    // === ODONTOGRAMA FORMSET ===
    let dienteSeleccionado = null;

    const botonesDientes = document.querySelectorAll('.diente-en-modal');
    const addFormBtnDiente = document.getElementById('add-form-btn');
    const estadoContainer = document.getElementById('estadoDiente-container');
    const emptyFormTemplateDiente = document.getElementById('empty-form-estadoDiente').innerHTML;
    const totalFormsDiente = document.querySelector('#id_estadodiente_set-TOTAL_FORMS');

    function resetFormularioDiente() {
        console.log("Reseteando formulario diente...");
        const selects = estadoContainer.querySelectorAll('select');
        selects.forEach(el => el.disabled = true);
        if (addFormBtnDiente) addFormBtnDiente.disabled = true;
    }

    function limpiarFormularioDienteCompleto() {
        console.log("Limpiando formulario odontograma COMPLETO...");
        estadoContainer.innerHTML = ""; // elimina todos los forms hijos
        totalFormsDiente.value = 0; // reinicia contador de forms
        dienteSeleccionado = null; // reinicia seleccion
        resetFormularioDiente(); // deshabilita select y botón agregar
    }

    resetFormularioDiente();

    botonesDientes.forEach(btn => {
        btn.addEventListener('click', function () {
            const numeroDiente = this.querySelector('.diente-label').textContent.trim();

            if (dienteSeleccionado && dienteSeleccionado !== numeroDiente) {
                if (!confirm("¿Está seguro de cambiar de diente? Se perderán los datos no guardados.")) {
                    return;
                }
                limpiarFormularioDienteCompleto();
            }

            dienteSeleccionado = numeroDiente;

            const selects = estadoContainer.querySelectorAll('select');
            selects.forEach(el => {
                el.disabled = false;
                setSelectDiente(el, numeroDiente);
            });

            if (addFormBtnDiente) addFormBtnDiente.disabled = false;

        });
    });

    window.addEstadoDienteForm = function () {
        const formIndex = parseInt(totalFormsDiente.value);
        const newForm = emptyFormTemplateDiente.replace(/__prefix__/g, formIndex);
        estadoContainer.insertAdjacentHTML('beforeend', newForm);
        totalFormsDiente.value = formIndex + 1;

        const newSelects = estadoContainer.querySelectorAll('select');
        const lastSelect = newSelects[newSelects.length - 1];

        setSelectDiente(lastSelect, dienteSeleccionado);
    };

    window.removeEstadoDienteForm = function (btn) {
        const formRow = btn.closest('.form-row');
        if (formRow) formRow.remove();
    };

    function setSelectDiente(select, numero) {
        if (!numero) {
            console.warn("Número de diente no definido");
            return;
        }
        select.value = numero;
        select.disabled = false;

        if (select.value !== numero) {
            console.warn(`No se encontró opción para el diente ${numero}`);
        } else {
            console.log(`Select seteado correctamente con diente ${numero}`);
        }
    }

    estadoContainer.addEventListener('click', function (e) {
        if (e.target.closest('.remove-form')) {
            e.target.closest('.form-row').remove();
        }
    });

    document.querySelector('form').addEventListener('submit', function() {
        const selects = estadoContainer.querySelectorAll('select');
        selects.forEach(el => el.disabled = false);
    });

    /** 🔥 Limpieza total al cerrar el modal **/

    $('#odontogramaModal').on('hidden.bs.modal', function () {
        console.log("Modal cerrado, limpiando formulario...");
        limpiarFormularioDienteCompleto();
    });
});
