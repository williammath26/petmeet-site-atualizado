// frontend/static/main.js

let currentSide = 1;

document.addEventListener('DOMContentLoaded', function () {
    const yellowPetLabelLeft = document.querySelector('.yellow-pet-label-left');

    // Verifica se o elemento existe antes de adicionar o ouvinte de evento
    if (yellowPetLabelLeft) {
        yellowPetLabelLeft.addEventListener('click', toggleLabelSide);
    }

    // Ao carregar a página, exibir o conteúdo associado ao "side1"
    updateLabelData();
    // Rotacionar o rótulo com base no lado inicial
    rotateLabel();
});

function toggleLabelSide() {
    // Alternar entre os lados
    currentSide = (currentSide === 1) ? 2 : 1;

    // Atualizar os dados do rótulo com base no lado atual
    updateLabelData();

    // Girar o rótulo
    rotateLabel();
}

function updateLabelData() {
    const side1Element = document.getElementById('side1');
    const side2Element = document.getElementById('side2');

    if (side1Element && side2Element) {
        if (currentSide === 1) {
            // Exibir o conteúdo associado ao "side1"
            side1Element.style.display = 'block';
            side2Element.style.display = 'none';

            // Atualizar dados do Lado 1 (Foto e Nome)
            const petName = document.getElementById('pet-name-side1');
            // Atualize petName com os dados relevantes
            petName.textContent = "Nome do Pet Lado 1"; // Substitua pelo dado real
        } else {
            // Exibir o conteúdo associado ao "side2"
            side1Element.style.display = 'none';
            side2Element.style.display = 'block';

            // Atualizar dados do Lado 2 (Detalhes do Pet)
            const petNameSide2 = document.getElementById('pet-name-side2');
            // Atualize petNameSide2 com os dados relevantes
            petNameSide2.textContent = "Nome do Pet Lado 2"; // Substitua pelo dado real
        }
    }
}

function rotateLabel() {
    const label = document.querySelector('.yellow-label-left');
    if (label) {
        label.style.transform = `rotate(${currentSide === 1 ? 0 : 180}deg)`;
    }
}

function performLogin() {
    // ... (código anterior para a função performLogin)
}

function performRegistration(event) {
    // ... (código anterior para a função performRegistration)
}

function createUserPet(user_id, petData) {
    // ... (código anterior para a função createUserPet)
}

function redirectToLogin() {
    // ... (código anterior para a função redirectToLogin)
}

function redirectToMain() {
    // ... (código anterior para a função redirectToMain)
}

// ... (funções adicionais, se houver)
function show() {
    const form = document.querySelector("#signup");
    form.classList.add("show");
    document.querySelector(".layer").style.display = "block";
}

const hide = () => {
    const hide = document.querySelector(".show")
    hide.classList.remove("show")
    document.querySelector(".layer").style.display="none"
}

document.addEventListener('DOMContentLoaded', function () {
    const yellowLabelLeft = document.querySelector('.yellow-label-left');

    // Verifica se o elemento existe antes de adicionar o ouvinte de evento
    if (yellowLabelLeft) {
        yellowLabelLeft.addEventListener('click', openPopup);
    }
});

function openPopup() {
    // Criar o pop-up (novo label amarelo)
    const popup = document.createElement('div');
    popup.className = 'yellow-popup';

    // Adicionar a imagem "FotoPet.png" na parte superior do pop-up
    const popupHeader = document.createElement('div');
    popupHeader.className = 'popup-header';

    // Adicionar o botão de fechar à direita
    const closeButton = document.createElement('div');
    closeButton.className = 'popup-close-button';
    closeButton.addEventListener('click', closePopup);
    popupHeader.appendChild(closeButton);

    const headerImage = document.createElement('img');
    headerImage.src = 'static/Img/FotoPet.png'; // Caminho relativo direto
    headerImage.alt = 'Foto do Pet';
    popupHeader.appendChild(headerImage);
    popup.appendChild(popupHeader);

    // Adicionar os textos e campos para preenchimento
    const popupContent = document.createElement('div');
    popupContent.className = 'popup-content';

    const textLabels = ['Nome', 'Raça', 'Peso', 'Idade', 'Data de Nasc.', 'Cor'];

    textLabels.forEach(label => {
        const labelText = document.createElement('div');
        labelText.textContent = label;
        popupContent.appendChild(labelText);

        const inputField = document.createElement('input');
        inputField.type = 'text';
        // Adicione classes, IDs ou outros atributos conforme necessário
        popupContent.appendChild(inputField);
    });

    popup.appendChild(popupContent);

    // Adicionar o botão "Salvar" abaixo da última caixa de texto
    const saveButton = document.createElement('button');
    saveButton.textContent = 'Salvar';
    saveButton.className = 'popup-save-button';
    saveButton.addEventListener('click', saveData); // Adicione a função de salvar dados
    popupContent.appendChild(saveButton);

    // Adicionar o pop-up à página
    document.body.appendChild(popup);
}

function closePopup() {
    // Lógica para fechar o pop-up.
    const popup = document.querySelector('.yellow-popup');
    document.body.removeChild(popup);
}

function saveData() {
    // Lógica para salvar os dados conforme necessário
    console.log('Dados salvos!');
    closePopup(); // Feche o pop-up após salvar os dados, se desejado
}
