// Booking functionality
document.addEventListener('DOMContentLoaded', function() {
    const skillData = window.skillData;

    // Initialize date picker
    const datePicker = flatpickr("#booking-date", {
        minDate: "today",
        enable: [
            function(date) {
                // Convert day to our format (Monday=1, Sunday=7)
                let day = date.getDay();
                day = day === 0 ? 7 : day;
                return skillData.availableDays.includes(day);
            }
        ],
        disable: skillData.unavailableSlots.map(slot => ({
            from: slot.from,
            to: slot.to
        }))
    });

    // Initialize time picker
    const timePicker = flatpickr("#booking-time", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        minTime: skillData.availableFrom,
        maxTime: skillData.availableTo,
        minuteIncrement: 30
    });

    // Modal functions
    window.openBookingModal = function() {
        document.getElementById('bookingModal').classList.remove('hidden');
    };

    window.closeBookingModal = function() {
        document.getElementById('bookingModal').classList.add('hidden');
    };

    // Update price calculation
    document.getElementById('duration').addEventListener('change', function(e) {
        const hours = parseInt(e.target.value);
        const total = hours * skillData.hourlyRate;
        document.getElementById('durationText').textContent = `${hours} hour${hours > 1 ? 's' : ''}`;
        document.getElementById('totalPrice').textContent = `R${total}`;
    });

    // Close modal when clicking outside
    document.getElementById('bookingModal').addEventListener('click', function(e) {
        if (e.target === this) {
            closeBookingModal();
        }
    });
});