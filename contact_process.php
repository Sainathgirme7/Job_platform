<?php
// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    // Get form input data
    $firstname = strip_tags(trim($_POST["firstname"]));
    $lastname = strip_tags(trim($_POST["lastname"]));
    $email = filter_var(trim($_POST["email"]), FILTER_SANITIZE_EMAIL);
    $subject = strip_tags(trim($_POST["subject"]));
    $message = trim($_POST["message"]);

    // Check if the fields are not empty
    if (empty($firstname) || empty($subject) || empty($message) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        // Error: All fields are required, and the email must be valid
        echo "<script>alert('Please fill out all fields and provide a valid email address.'); window.history.back();</script>";
        exit;
    }

    // Set the recipient email address
    $recipient = "sainathgirme06@gmail.com"; // Replace with your email address

    // Set the email subject
    $email_subject = "New Contact Form Message from $firstname $lastname";

    // Build the email content
    $email_content = "First Name: $firstname\n";
    $email_content .= "Last Name: $lastname\n";
    $email_content .= "Email: $email\n\n";
    $email_content .= "Subject: $subject\n\n";
    $email_content .= "Message:\n$message\n";

    // Set the email headers
    $email_headers = "From: $firstname $lastname <$email>";

    // Send the email
    if (mail($recipient, $email_subject, $email_content, $email_headers)) {
        // Success: Display a success message
        echo "<script>alert('Your message has been sent successfully!'); window.location.href = 'contact.html';</script>";
    } else {
        // Error: Display an error message
        echo "<script>alert('Oops! Something went wrong, and we couldn\'t send your message. Please try again later.'); window.history.back();</script>";
    }
}
?>
