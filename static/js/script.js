const form = document.querySelector('#form');
const loader = document.querySelector('#loader');
const select_titular = document.querySelector('#id_holder');
const beneficiario_form = document.querySelector('#beneficiario_form');
const id_mail = document.querySelector('#id_mail');
const id_beneficiary_document = document.querySelector('#id_beneficiary_document');
const id_beneficiary_name = document.querySelector('#id_beneficiary_name');
const id_beneficiary_last_name = document.querySelector('#id_beneficiary_last_name');
const id_beneficiary_birth_date = document.querySelector('#id_beneficiary_birth_date');
const id_beneficiary_phone = document.querySelector('#id_beneficiary_phone');
const id_beneficiary_email = document.querySelector('#id_beneficiary_email');
const id_beneficiary_relationship = document.querySelector('#id_beneficiary_relationship');
form.addEventListener('submit', (e) => {
    e.preventDefault();
    loader.removeAttribute('hidden');
    form.submit();
});

select_titular.addEventListener('change', function(event) {
  if (event.target.value === 'No') {
    beneficiario_form.style.display = 'block';
    id_mail.style.display = 'hidden';
  } else {
    beneficiario_form.style.display = 'none';
    // Remover el atributo 'required' de todos los elementos
    id_beneficiary_document?.removeAttribute('required');
    id_beneficiary_name?.removeAttribute('required');
    id_beneficiary_last_name?.removeAttribute('required');
    id_beneficiary_birth_date?.removeAttribute('required');
    id_beneficiary_phone?.removeAttribute('required');
    id_beneficiary_email?.removeAttribute('required');
    id_beneficiary_relationship?.removeAttribute('required');
    id_mail?.removeAttribute('required');
  }
});
