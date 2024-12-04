// Image upload handling
function initializeImageUpload() {
    const dropZone = document.querySelector('.image-upload-area');
    const fileInput = document.querySelector('input[type="file"]');
    const previewContainer = document.querySelector('.preview-grid') || document.createElement('div');
    
    if (!document.querySelector('.preview-grid')) {
        previewContainer.className = 'mt-4 grid grid-cols-2 gap-4 sm:grid-cols-3';
        dropZone.parentElement.appendChild(previewContainer);
    }

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop zone when dragging over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    // Handle dropped files
    dropZone.addEventListener('drop', handleDrop, false);
    fileInput.addEventListener('change', handleFiles, false);

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight(e) {
        dropZone.classList.add('border-indigo-500', 'bg-indigo-50');
    }

    function unhighlight(e) {
        dropZone.classList.remove('border-indigo-500', 'bg-indigo-50');
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles({ target: { files } });
    }

    function handleFiles(e) {
        const files = [...e.target.files];
        files.forEach(previewFile);
    }

    function previewFile(file) {
        if (!file.type.startsWith('image/')) return;

        const reader = new FileReader();
        reader.readAsDataURL(file);
        
        reader.onload = function() {
            const preview = document.createElement('div');
            preview.className = 'relative rounded-lg overflow-hidden group aspect-w-16 aspect-h-9';
            preview.innerHTML = `
                <img src="${reader.result}" alt="Preview" class="w-full h-full object-cover">
                <div class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-200">
                    <button type="button" class="text-white hover:text-red-500 transition-colors p-2 rounded-full hover:bg-white/10">
                        <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                    </button>
                </div>
            `;

            // Add delete functionality
            const deleteBtn = preview.querySelector('button');
            deleteBtn.addEventListener('click', () => {
                preview.remove();
                // Here you would also want to update the actual file input
                // This is a simplified version
            });

            previewContainer.appendChild(preview);
        };
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeImageUpload);