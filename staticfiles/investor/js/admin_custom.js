document.addEventListener('DOMContentLoaded', function() {
    console.log('Admin custom JS loaded');
    
    // Add style to make action buttons more visible
    const style = document.createElement('style');
    style.textContent = `
        .action-button {
            font-weight: bold !important;
            padding: 10px 15px !important;
            margin: 5px !important;
            border-radius: 5px !important;
        }
        .action-approve {
            background-color: #28a745 !important;
            color: white !important;
            border: 2px solid #1e7e34 !important;
        }
        .action-reject {
            background-color: #dc3545 !important;
            color: white !important;
            border: 2px solid #c82333 !important;
        }
        .action-section {
            background-color: #f8f9fa;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
            border: 1px solid #dee2e6;
        }
    `;
    document.head.appendChild(style);
    
    // Function to enhance action dropdown
    function enhanceActionDropdown() {
        const actionSelect = document.querySelector('select[name="action"]');
        const goButton = document.querySelector('button[type="submit"].default');
        
        if (actionSelect && goButton) {
            console.log('Action dropdown and Go button found');
            
            // Create quick action buttons
            const actionSection = document.createElement('div');
            actionSection.className = 'action-section';
            actionSection.innerHTML = `
                <h3 style="margin-top: 0;">Quick Actions</h3>
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <button type="button" class="action-button action-approve" data-action="approve_investments">
                        ✅ Approve Selected
                    </button>
                    <button type="button" class="action-button action-reject" data-action="reject_investments">
                        ❌ Reject Selected
                    </button>
                </div>
                <p style="color: #6c757d; margin-top: 10px; font-size: 14px;">
                    Select items using checkboxes, then click an action button.
                </p>
            `;
            
            // Insert after the action dropdown
            const actionsContainer = actionSelect.closest('.actions');
            if (actionsContainer) {
                actionsContainer.appendChild(actionSection);
                
                // Add event listeners to quick action buttons
                document.querySelectorAll('[data-action]').forEach(button => {
                    button.addEventListener('click', function() {
                        const action = this.getAttribute('data-action');
                        actionSelect.value = action;
                        goButton.click();
                    });
                });
            }
        }
    }
    
    // Check if we're on investment or withdrawal page and enhance accordingly
    if (window.location.href.includes('/investor/investment/')) {
        enhanceActionDropdown();
        
        // Modify action labels for investments
        setTimeout(() => {
            const options = document.querySelectorAll('select[name="action"] option');
            options.forEach(option => {
                if (option.value === 'approve_investments') {
                    option.textContent = '✅ APPROVE SELECTED INVESTMENTS';
                } else if (option.value === 'reject_investments') {
                    option.textContent = '❌ REJECT SELECTED INVESTMENTS';
                }
            });
        }, 100);
        
    } else if (window.location.href.includes('/investor/withdrawal/')) {
        enhanceActionDropdown();
        
        // Modify action labels for withdrawals
        setTimeout(() => {
            const options = document.querySelectorAll('select[name="action"] option');
            options.forEach(option => {
                if (option.value === 'process_withdrawals') {
                    option.textContent = '✅ PROCESS SELECTED WITHDRAWALS';
                } else if (option.value === 'cancel_withdrawals') {
                    option.textContent = '❌ CANCEL SELECTED WITHDRAWALS';
                }
            });
        }, 100);
    }
    
    // Also add individual item action buttons
    function addIndividualActionButtons() {
        const submitRow = document.querySelector('.submit-row');
        if (submitRow) {
            // Check if we're on investment or withdrawal detail page
            if (window.location.href.includes('/investor/investment/') && 
                !window.location.href.includes('/add/')) {
                
                const approvedCheckbox = document.querySelector('input[name="approved"]');
                if (approvedCheckbox) {
                    const buttonDiv = document.createElement('div');
                    buttonDiv.className = 'action-section';
                    buttonDiv.innerHTML = `
                        <h3 style="margin-top: 0;">Quick Approval</h3>
                        <div style="display: flex; gap: 10px;">
                            <button type="button" class="action-button action-approve" id="quick-approve">
                                ✅ Approve This Investment
                            </button>
                            <button type="button" class="action-button action-reject" id="quick-reject">
                                ❌ Reject This Investment
                            </button>
                        </div>
                    `;
                    
                    submitRow.parentNode.insertBefore(buttonDiv, submitRow);
                    
                    document.getElementById('quick-approve').addEventListener('click', function() {
                        approvedCheckbox.checked = true;
                        document.querySelector('input[name="_save"]').click();
                    });
                    
                    document.getElementById('quick-reject').addEventListener('click', function() {
                        approvedCheckbox.checked = false;
                        document.querySelector('input[name="_save"]').click();
                    });
                }
            }
        }
    }
    
    addIndividualActionButtons();
});
