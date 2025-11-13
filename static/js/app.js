// Global variables
let allJobcards = [];
let filteredJobcards = [];
let metadata = {};
let currentEditIndex = -1;

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    loadMetadata();
    loadJobcards();
    
    // Setup event listeners
    document.getElementById('checkTypeFilter').addEventListener('change', applyFilters);
    document.getElementById('aircraftFilter').addEventListener('change', applyFilters);
    document.getElementById('searchInput').addEventListener('input', applyFilters);
    document.getElementById('jobcardForm').addEventListener('submit', handleFormSubmit);
});

// Load metadata (check types, aircraft)
async function loadMetadata() {
    try {
        const response = await fetch('/api/metadata');
        const result = await response.json();
        
        if (result.success) {
            metadata = result.data;
            
            // Populate check type filter
            const checkTypeFilter = document.getElementById('checkTypeFilter');
            checkTypeFilter.innerHTML = '<option value="All">All</option>';
            metadata.check_types.forEach(type => {
                checkTypeFilter.innerHTML += `<option value="${type}">${type}</option>`;
            });
            
            // Populate aircraft filter
            const aircraftFilter = document.getElementById('aircraftFilter');
            aircraftFilter.innerHTML = '<option value="All">All</option>';
            metadata.aircraft.forEach(ac => {
                aircraftFilter.innerHTML += `<option value="${ac}">${ac}</option>`;
            });
            
            // Populate form check type
            const checkTypeForm = document.getElementById('checkType');
            checkTypeForm.innerHTML = '<option value="">Select...</option>';
            metadata.check_types.forEach(type => {
                checkTypeForm.innerHTML += `<option value="${type}">${type}</option>`;
            });
            
            // Create aircraft status fields
            const aircraftStatusFields = document.getElementById('aircraftStatusFields');
            aircraftStatusFields.innerHTML = '';
            metadata.aircraft.forEach(ac => {
                aircraftStatusFields.innerHTML += `
                    <div class="form-group">
                        <label for="status_${ac}">${ac}:</label>
                        <input type="text" id="status_${ac}" placeholder="Status for ${ac}">
                    </div>
                `;
            });
        }
    } catch (error) {
        console.error('Error loading metadata:', error);
        updateStatus('Error loading metadata', 'error');
    }
}

// Load job cards
async function loadJobcards() {
    try {
        updateStatus('Loading job cards...');
        
        const checkType = document.getElementById('checkTypeFilter').value;
        const aircraft = document.getElementById('aircraftFilter').value;
        const search = document.getElementById('searchInput').value;
        
        const params = new URLSearchParams();
        if (checkType !== 'All') params.append('check_type', checkType);
        if (aircraft !== 'All') params.append('aircraft', aircraft);
        if (search) params.append('search', search);
        
        const response = await fetch(`/api/jobcards?${params}`);
        const result = await response.json();
        
        if (result.success) {
            allJobcards = result.data;
            filteredJobcards = result.data;
            displayJobcards();
            updateStatus(`Showing ${result.total} job cards`);
        } else {
            updateStatus('Error loading job cards: ' + result.error, 'error');
        }
    } catch (error) {
        console.error('Error loading job cards:', error);
        updateStatus('Error loading job cards', 'error');
    }
}

// Display job cards in table
function displayJobcards() {
    const tbody = document.getElementById('tableBody');
    
    if (filteredJobcards.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="loading">No job cards found</td></tr>';
        return;
    }
    
    tbody.innerHTML = '';
    filteredJobcards.forEach((jc, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${jc['CHECK TYPE'] || ''}</td>
            <td>${jc['ITEM NO'] || ''}</td>
            <td>${jc['CARD NUMBER1'] || ''}</td>
            <td>${jc['TASK REFERENCE'] || ''}</td>
            <td>${jc['TASK TITLE'] || ''}</td>
            <td>${jc['ZONE'] || ''}</td>
            <td>${jc['A/C TYPE'] || ''}</td>
            <td>${jc['TYPE OF INSP'] || ''}</td>
            <td class="action-buttons">
                <button class="btn btn-info btn-small" onclick="editJobcard(${index})">Edit</button>
                <button class="btn btn-danger btn-small" onclick="deleteJobcard(${index})">Delete</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Apply filters
function applyFilters() {
    loadJobcards();
}

// Clear filters
function clearFilters() {
    document.getElementById('checkTypeFilter').value = 'All';
    document.getElementById('aircraftFilter').value = 'All';
    document.getElementById('searchInput').value = '';
    loadJobcards();
}

// Show add dialog
function showAddDialog() {
    currentEditIndex = -1;
    document.getElementById('modalTitle').textContent = 'Add Job Card';
    document.getElementById('jobcardForm').reset();
    document.getElementById('jobcardIndex').value = '';
    document.getElementById('jobcardModal').style.display = 'block';
}

// Edit job card
async function editJobcard(index) {
    try {
        const jobcard = filteredJobcards[index];
        
        // Find actual index in all jobcards
        const actualIndex = allJobcards.findIndex(jc => 
            jc['CARD NUMBER1'] === jobcard['CARD NUMBER1'] && 
            jc['ITEM NO'] === jobcard['ITEM NO']
        );
        
        currentEditIndex = actualIndex;
        
        document.getElementById('modalTitle').textContent = 'Edit Job Card';
        document.getElementById('jobcardIndex').value = actualIndex;
        
        // Populate form
        document.getElementById('checkType').value = jobcard['CHECK TYPE'] || '';
        document.getElementById('itemNo').value = jobcard['ITEM NO'] || '';
        document.getElementById('cardNumber').value = jobcard['CARD NUMBER1'] || '';
        document.getElementById('taskReference').value = jobcard['TASK REFERENCE'] || '';
        document.getElementById('taskTitle').value = jobcard['TASK TITLE'] || '';
        document.getElementById('description').value = jobcard['DESCRIPTION'] || '';
        document.getElementById('zone').value = jobcard['ZONE'] || '';
        document.getElementById('acType').value = jobcard['A/C TYPE'] || '';
        document.getElementById('typeOfInsp').value = jobcard['TYPE OF INSP'] || '';
        
        // Populate aircraft status
        metadata.aircraft.forEach(ac => {
            const field = document.getElementById(`status_${ac}`);
            if (field) {
                field.value = jobcard[ac] || '';
            }
        });
        
        document.getElementById('jobcardModal').style.display = 'block';
    } catch (error) {
        console.error('Error editing job card:', error);
        alert('Error loading job card data');
    }
}

// Delete job card
async function deleteJobcard(index) {
    if (!confirm('Are you sure you want to delete this job card?')) {
        return;
    }
    
    try {
        const jobcard = filteredJobcards[index];
        
        // Find actual index in all jobcards
        const actualIndex = allJobcards.findIndex(jc => 
            jc['CARD NUMBER1'] === jobcard['CARD NUMBER1'] && 
            jc['ITEM NO'] === jobcard['ITEM NO']
        );
        
        const response = await fetch(`/api/jobcards/${actualIndex}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            updateStatus('Job card deleted successfully');
            loadJobcards();
        } else {
            alert('Error deleting job card: ' + result.error);
        }
    } catch (error) {
        console.error('Error deleting job card:', error);
        alert('Error deleting job card');
    }
}

// Handle form submit
async function handleFormSubmit(e) {
    e.preventDefault();
    
    try {
        const formData = {
            'CHECK TYPE': document.getElementById('checkType').value,
            'ITEM NO': parseInt(document.getElementById('itemNo').value),
            'CARD NUMBER1': document.getElementById('cardNumber').value,
            'TASK REFERENCE': document.getElementById('taskReference').value,
            'TASK TITLE': document.getElementById('taskTitle').value,
            'DESCRIPTION': document.getElementById('description').value,
            'ZONE': document.getElementById('zone').value,
            'A/C TYPE': document.getElementById('acType').value,
            'TYPE OF INSP': document.getElementById('typeOfInsp').value
        };
        
        // Add aircraft status
        metadata.aircraft.forEach(ac => {
            const field = document.getElementById(`status_${ac}`);
            if (field && field.value) {
                formData[ac] = field.value;
            }
        });
        
        let response;
        if (currentEditIndex >= 0) {
            // Update existing
            response = await fetch(`/api/jobcards/${currentEditIndex}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
        } else {
            // Add new
            response = await fetch('/api/jobcards', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
        }
        
        const result = await response.json();
        
        if (result.success) {
            updateStatus(result.message);
            closeModal();
            loadJobcards();
        } else {
            alert('Error saving job card: ' + result.error);
        }
    } catch (error) {
        console.error('Error saving job card:', error);
        alert('Error saving job card');
    }
}

// Close modal
function closeModal() {
    document.getElementById('jobcardModal').style.display = 'none';
}

// Save changes to database
async function saveChanges() {
    if (!confirm('Save all changes to the database?')) {
        return;
    }
    
    try {
        updateStatus('Saving changes...');
        
        const response = await fetch('/api/save', {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            updateStatus('Changes saved successfully');
        } else {
            alert('Error saving changes: ' + result.error);
        }
    } catch (error) {
        console.error('Error saving changes:', error);
        alert('Error saving changes');
    }
}

// Export data
async function exportData() {
    try {
        updateStatus('Exporting data...');
        
        // Get indices of filtered jobcards
        const indices = filteredJobcards.map(jc => {
            return allJobcards.findIndex(ajc => 
                ajc['CARD NUMBER1'] === jc['CARD NUMBER1'] && 
                ajc['ITEM NO'] === jc['ITEM NO']
            );
        });
        
        const response = await fetch('/api/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ indices })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'jobcards_export.xlsx';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            updateStatus('Data exported successfully');
        } else {
            alert('Error exporting data');
        }
    } catch (error) {
        console.error('Error exporting data:', error);
        alert('Error exporting data');
    }
}

// Refresh data
function refreshData() {
    loadMetadata();
    loadJobcards();
}

// Update status bar
function updateStatus(message, type = 'info') {
    const statusText = document.getElementById('statusText');
    statusText.textContent = message;
    
    const statusBar = document.getElementById('statusBar');
    statusBar.style.background = type === 'error' ? '#f8d7da' : '#e7f3ff';
    statusText.style.color = type === 'error' ? '#721c24' : '#004085';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('jobcardModal');
    if (event.target === modal) {
        closeModal();
    }
}
