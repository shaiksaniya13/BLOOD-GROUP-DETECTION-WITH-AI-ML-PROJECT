const imageUpload = document.getElementById('imageUpload');
const preview = document.getElementById('preview');
const detectBtn = document.getElementById('detectBtn');
const result = document.getElementById('result');
const bloodGroupSpan = document.getElementById('bloodGroup');
const confidenceDiv = document.getElementById('confidence');  // New div to show confidence

const bloodColors = {
  'A': 'bg-red-200 text-red-800',
  'B': 'bg-blue-200 text-blue-800',
  'AB': 'bg-purple-200 text-purple-800',
  'O': 'bg-green-200 text-green-800'
};

imageUpload.addEventListener('change', function() {
  const file = this.files[0];
  if(file){
    preview.src = URL.createObjectURL(file);
    preview.classList.remove('hidden');
  }
});

detectBtn.addEventListener('click', async function() {
  if(!imageUpload.files[0]){
    alert("Please upload an image first!");
    return;
  }

  const formData = new FormData();
  formData.append('file', imageUpload.files[0]);

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    if(data.blood_group){
      const bloodGroup = data.blood_group;
      bloodGroupSpan.textContent = bloodGroup;

      // Show confidence for all blood groups
      let confidenceText = '';
      for (let bg in data.confidence) {
        confidenceText += `${bg}: ${data.confidence[bg]}%<br>`;
      }
      confidenceDiv.innerHTML = confidenceText;

      result.className = `mt-6 p-4 rounded-lg text-xl font-bold relative z-10 transition duration-500 ${bloodColors[bloodGroup]}`;
      result.classList.remove('hidden');
      result.animate([{opacity:0, transform:'translateY(-20px)'}, {opacity:1, transform:'translateY(0)'}], {duration:500, fill:'forwards'});
    } else {
      alert("Prediction failed!");
    }
  } catch (error) {
    console.error(error);
    alert("Error connecting to the server.");
  }
});

