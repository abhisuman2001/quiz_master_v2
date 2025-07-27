import { createRouter, createWebHistory } from 'vue-router'
import { jwtDecode } from 'jwt-decode'; // Import the decoder
import HomePage from '../views/HomePage.vue'
import AdminLayout from '../layouts/AdminLayout.vue' // Import the new layout

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  
  // --- THIS IS THE UPDATED ADMIN ROUTING BLOCK ---
  {
    path: '/admin',
    component: AdminLayout, // The parent route uses the layout
    meta: { requiresAuth: true, role: 'admin' }, // Protection applies to all child routes
    children: [
      {
        // Path becomes /admin/dashboard
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('../views/AdminDashboard.vue')
      },
      {
        // Path becomes /admin/subjects
        path: 'subjects',
        name: 'SubjectManagement',
        component: () => import('../views/admin/SubjectManagement.vue')
      }
      // You can add more admin pages here later (e.g., 'quizzes', 'users')
    ]
  },
  // ---------------------------------------------

  {
    path: '/dashboard',
    name: 'UserDashboard',
    component: () => import('../views/UserDashboard.vue'),
    meta: { requiresAuth: true, role: 'user' } 
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// --- Navigation Guard (remains the same) ---
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('accessToken');
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  if (requiresAuth && !token) {
    // If route requires auth and there's no token, redirect to login
    next('/login');
  } else if (token) {
    const userData = jwtDecode(token); // Decode token to get user role
    const userRole = userData.sub.role;

    // If the route has meta and the user's role doesn't match the required role
    if (to.meta.role && to.meta.role !== userRole) {
      // Redirect based on their actual role
      if (userRole === 'admin') {
        next('/admin/dashboard');
      } else {
        next('/dashboard');
      }
    } else {
      // User has the correct role, or route doesn't require a specific role
      next();
    }
  } else {
    // Route doesn't require auth
    next();
  }
});


export default router