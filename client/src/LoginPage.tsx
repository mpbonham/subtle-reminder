import { Button } from '@mui/material';
import './LoginPage.scss';

function LoginPage() {
  return (
    <div id="login-page-container">
      <div id="login-page-top">
        <h1>Sign in to Subtle Reminder</h1>
        <p>By signing in, you agree to Subtle Map's Privacy Policy.</p>
      </div>
      <div id="login-page-bottom">
        <Button
          variant="contained"
          disableElevation
          id="login-page-button"
          href="/login"
        >
          Continue with Google
        </Button>
      </div>
    </div>
  );
}

export default LoginPage;
