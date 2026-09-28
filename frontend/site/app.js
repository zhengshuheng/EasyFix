/* ===== 易学习 EasyStudy 官网脚本：账号注册 / 登录 / 我的空间 =====
 * 账号/空间分离流程：
 *   注册账号 → 「我的空间」面板 → 创建体验空间 / 进入已有空间 / 下载本地版
 * 空间内前端（dist-trial）读取 localStorage：easyfix_token / easyfix_user / easyfix_trial_key
 */
(function () {
  'use strict';

  var API = '/api/account';
  var TRIAL_API = '/api/trial';
  var SUB_API = '/api/subscription';
  var CONFIG_API = '/api/config';

  // ---------- 元素 ----------
  var tabs = document.querySelectorAll('.tab');
  var registerForm = document.getElementById('registerForm');
  var loginForm = document.getElementById('loginForm');
  var formMsg = document.getElementById('formMsg');
  var regRole = document.getElementById('regRole');
  var panel = document.getElementById('spacePanel');
  var panelUsername = document.getElementById('spaceUsername');
  var spaceReady = document.getElementById('spaceReady');
  var spaceEmpty = document.getElementById('spaceEmpty');
  var spaceEnterBtn = document.getElementById('spaceEnterBtn');
  var spaceCreateBtn = document.getElementById('spaceCreateBtn');
  var spaceChildName = document.getElementById('spaceChildName');
  var spaceChildNameWrap = document.getElementById('spaceChildNameWrap');
  var spaceLogout = document.getElementById('spaceLogout');
  var spaceStatus = document.getElementById('spaceStatus');
  var spaceStatusText = document.getElementById('spaceStatusText');
  var spaceUpgradeBtn = document.getElementById('spaceUpgradeBtn');
  var upgradeModal = document.getElementById('upgradeModal');
  var upgradeClose = document.getElementById('upgradeClose');
  var upgradeMsg = document.getElementById('upgradeMsg');
  var planOnline = document.getElementById('planOnline');
  var planLocal = document.getElementById('planLocal');
  var onlinePrice = document.getElementById('onlinePrice');
  var localPrice = document.getElementById('localPrice');
  var payZone = document.getElementById('payZone');
  var payAmount = document.getElementById('payAmount');
  var payDoneBtn = document.getElementById('payDoneBtn');
  var navToggle = document.querySelector('.nav-toggle');
  var navLinks = document.querySelector('.nav-links');

  // 当前选中的升级套餐
  var currentPlan = 'online';
  // 公开配置缓存（价格/天数）
  var publicConfig = { trial_days: 15, online_price: 100, local_price: 50 };

  // ---------- Tab 切换 ----------
  var tabsWrap = document.querySelector('.tabs');
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      // 回到表单态：隐藏面板（防止表单与面板叠加）
      panel.hidden = true;
      if (tabsWrap) tabsWrap.hidden = false;
      tabs.forEach(function (t) { t.classList.remove('on'); });
      tab.classList.add('on');
      var target = tab.dataset.tab;
      registerForm.classList.toggle('on', target === 'register');
      loginForm.classList.toggle('on', target === 'login');
      formMsg.textContent = '';
      formMsg.className = 'form-msg';
    });
  });

  // ---------- 直达 Tab：导航/hero 的「登录」按钮 → 切到对应 Tab 并滚到表单 ----------
  document.querySelectorAll('[data-goto-tab]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var target = a.getAttribute('data-goto-tab');
      tabs.forEach(function (t) { if (t.dataset.tab === target) t.click(); });
      var trialCard = document.getElementById('trial');
      if (trialCard && trialCard.scrollIntoView) trialCard.scrollIntoView({ behavior: 'smooth' });
    });
  });

  // ---------- URL 指定初始 Tab：如退出登录回官网 #trial?tab=login → 直接激活登录表单 ----------
  (function () {
    var m = (location.hash || '').match(/[?&]tab=(\w+)/);
    if (m) {
      var want = m[1];
      tabs.forEach(function (t) { if (t.dataset.tab === want) t.click(); });
    }
  })();

  // ---------- 移动端导航 ----------
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function () {
      navLinks.classList.toggle('open');
    });
  }

  // ---------- 工具 ----------
  function showMsg(text, ok) {
    formMsg.textContent = text;
    formMsg.className = 'form-msg ' + (ok ? 'ok' : 'err');
  }

  function clearMsg() {
    formMsg.textContent = '';
    formMsg.className = 'form-msg';
  }

  // ---------- 注册安全规则（与后端一致，前置拦截） ----------
  function validateRegister(username, password) {
    if (!/^1[3-9]\d{9}$/.test(username)) {
      return '请输入 11 位大陆手机号';
    }
    if (password.length < 8 || password.length > 20) {
      return '密码需 8-20 位';
    }
    if (!/([A-Za-z].*\d|\d.*[A-Za-z])/.test(password)) {
      return '密码需同时包含字母和数字';
    }
    if (/(.)\1{2,}/.test(password)) {
      return '密码不能包含连续 3 个相同字符';
    }
    if (username.toLowerCase() && password.toLowerCase().indexOf(username.toLowerCase()) !== -1) {
      return '密码不能包含用户名';
    }
    return '';
  }

  function post(path, data, token) {
    var headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = 'Bearer ' + token;
    return fetch(path, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(data),
    }).then(function (res) {
      return res.json().then(function (body) {
        if (!res.ok) {
          var err = new Error((body && body.detail) || '请求失败');
          err.status = res.status;
          throw err;
        }
        return body;
      });
    });
  }

  function getJSON(path, token) {
    return fetch(path, {
      headers: { 'Authorization': 'Bearer ' + token },
    }).then(function (res) {
      return res.json().then(function (body) {
        if (!res.ok) {
          var err = new Error((body && body.detail) || '请求失败');
          err.status = res.status;
          throw err;
        }
        return body;
      });
    });
  }

  function getToken() {
    // 官网面板 API（升级/订阅/我的空间）用 account token；空间内 API 用 easyfix_token
    return localStorage.getItem('easyfix_account_token');
  }

  // ---------- 我的空间面板（欢迎过渡页） ----------
  function showPanel(username) {
    clearMsg();
    registerForm.classList.remove('on');
    loginForm.classList.remove('on');
    // 面板态：隐藏 tab（注册/登录后进入「欢迎过渡」，不再显示切换入口）
    if (tabsWrap) tabsWrap.hidden = true;
    panel.hidden = false;
    panelUsername.textContent = username || '朋友';
    // 让「立即体验」CTA 落回表单（面板态下 Tab 不可见）
    // 平滑滚动到面板，营造「跳转到过渡页」的感觉
    try {
      panel.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } catch (e) { /* 老浏览器忽略 */ }
  }

  function showForms() {
    panel.hidden = true;
    if (tabsWrap) tabsWrap.hidden = false;
    registerForm.classList.add('on');
    loginForm.classList.remove('on');
  }

  function getSavedUser() {
    try { return JSON.parse(localStorage.getItem('easyfix_user') || 'null'); } catch (e) { return null; }
  }

  // 注册已填小孩昵称 → 创建空间不重复填：隐藏输入框、按钮带名字
  function presetChildName(user) {
    var saved = user || getSavedUser();
    var name = saved && saved.child_name ? String(saved.child_name).trim() : '';
    if (!name || !spaceChildNameWrap) return;
    spaceChildNameWrap.style.display = 'none';
    spaceCreateBtn.textContent = '创建「' + name + '」的体验空间 →';
    spaceChildName.value = name;
  }

  function renderSpace(space) {
    if (space && space.key) {
      spaceReady.hidden = false;
      spaceEmpty.hidden = true;
      spaceEnterBtn.textContent = '进入体验空间 →';
      spaceEnterBtn.onclick = function () {
        localStorage.setItem('easyfix_trial_key', space.key);
        if (!localStorage.getItem('easyfix_token')) {
          // 空间 token 缺失（如曾在空间端退出，官网账号 token 残留）：需要重新登录
          localStorage.removeItem('easyfix_account_token');
          localStorage.removeItem('easyfix_user');
          showMsg('登录状态已失效，请重新登录', false);
          setTimeout(function () { window.location.href = '/site/#trial?tab=login'; }, 900);
          return;
        }
        window.location.href = space.url;
      };
    } else {
      spaceReady.hidden = true;
      spaceEmpty.hidden = false;
    }
  }

  // ---------- 订阅/体验状态 ----------
  function loadPublicConfig() {
    return fetch(CONFIG_API + '/public').then(function (res) {
      return res.json();
    }).then(function (cfg) {
      if (cfg) {
        publicConfig = cfg;
        onlinePrice.textContent = '¥' + cfg.online_price;
        localPrice.textContent = '¥' + cfg.local_price;
        // 同步本地部署区/FAQ 的价格展示（运营后台可改）
        var dp = document.getElementById('downloadPrice');
        if (dp) dp.textContent = cfg.local_price;
        var fp = document.querySelectorAll('.faqPrice');
        for (var i = 0; i < fp.length; i++) fp[i].textContent = cfg.local_price;
      }
    }).catch(function () { /* 网络失败用默认值 */ });
  }

  function daysBetween(endStr) {
    if (!endStr) return null;
    var end = new Date(String(endStr).replace(' ', 'T'));
    if (isNaN(end.getTime())) return null;
    return Math.max(0, Math.ceil((end.getTime() - Date.now()) / 86400000));
  }

  function refreshStatus(user, space) {
    var plan = user && user.subscription_plan;
    var isPro = plan === 'pro_online' || plan === 'pro_local';
    spaceStatus.hidden = false;
    spaceUpgradeBtn.hidden = false;
    if (isPro) {
      spaceStatusText.textContent = '✅ 已是正式版（' + (plan === 'pro_online' ? '云端' : '本地') + '），不受体验期限制';
      spaceUpgradeBtn.hidden = true;
      return;
    }
    var end = space && space.trial_end_at;
    var days = daysBetween(end);
    if (days === null || days === undefined) {
      spaceStatusText.textContent = '体验空间创建后将开始计算 15 天免费体验';
      spaceUpgradeBtn.hidden = true;
      return;
    }
    if (days <= 0) {
      spaceStatusText.textContent = '⚠️ 体验期已结束，升级正式版后继续使用';
    } else {
      spaceStatusText.textContent = '⏳ 免费体验剩余 ' + days + ' 天（共 ' + publicConfig.trial_days + ' 天）';
    }
  }

  function enterPanelFromAccount(token, user) {
    // 已在登录态：查询账号 + 名下空间
    getJSON(API + '/me', token).then(function (r) {
      // 有空间则同步空间 token：面板「进入体验空间」直接进，不被登录墙拦截
      if (r.space_token) localStorage.setItem('easyfix_token', r.space_token);
      showPanel((r.user && r.user.username) || (user && user.username));
      presetChildName(r.user);
      renderSpace(r.space);
      refreshStatus(r.user, r.space);
    }).catch(function () {
      // token 失效：退回表单
      localStorage.removeItem('easyfix_token');
      localStorage.removeItem('easyfix_account_token');
      localStorage.removeItem('easyfix_user');
      showForms();
    });
  }

  // ---------- 升级弹层 ----------
  function openUpgrade() {
    upgradeMsg.textContent = '';
    upgradeMsg.className = 'form-msg';
    currentPlan = 'online';
    planOnline.classList.add('on');
    planLocal.classList.remove('on');
    payZone.hidden = false;
    payAmount.textContent = '¥' + publicConfig.online_price;
    upgradeModal.hidden = false;
  }

  function closeUpgrade() {
    upgradeModal.hidden = true;
    payZone.hidden = true;
  }

  upgradeClose.addEventListener('click', closeUpgrade);
  upgradeModal.addEventListener('click', function (e) {
    if (e.target === upgradeModal) closeUpgrade();
  });

  function selectPlan(planEl, plan) {
    planOnline.classList.toggle('on', plan === 'online');
    planLocal.classList.toggle('on', plan === 'local');
    currentPlan = plan;
    payAmount.textContent = '¥' + (plan === 'online' ? publicConfig.online_price : publicConfig.local_price);
  }

  planOnline.addEventListener('click', function () { selectPlan(planOnline, 'online'); });
  planLocal.addEventListener('click', function () { selectPlan(planLocal, 'local'); });

  spaceUpgradeBtn.addEventListener('click', openUpgrade);

  function finishPay() {
    var token = getToken();
    if (!token) { closeUpgrade(); showForms(); return; }
    var btn = payDoneBtn;
    btn.disabled = true;
    btn.textContent = '正在开通…';
    post(SUB_API + '/upgrade', { plan: currentPlan }, token)
      .then(function (r) {
        closeUpgrade();
        btn.disabled = false;
        btn.textContent = '✅ 我已支付完成';
        var planName = r.subscription_plan === 'pro_online' ? '云端正式版' : '本地正式版';
        showMsg('🎉 ' + planName + ' 开通成功！', true);
        if (currentPlan === 'local') {
          if (r.download_url) {
            showMsg('🎉 本地版开通成功！' + (r.guide_url ? '安装指引见下。' : '请下载本地版安装包。'), true);
            var a = document.createElement('a');
            a.href = r.download_url;
            a.className = 'space-more-link';
            a.textContent = '⬇ 下载本地部署版';
            panel.appendChild(a);
            setTimeout(function () {
              if (a.parentNode) a.parentNode.removeChild(a);
            }, 30000);
          }
        }
        // 刷新面板：转正式 + 刷新用户信息
        return getJSON(API + '/me', token);
      })
      .then(function (r2) {
        if (!r2) return;
        localStorage.setItem('easyfix_user', JSON.stringify(r2.user));
        renderSpace(r2.space);
        refreshStatus(r2.user, r2.space);
      })
      .catch(function (err) {
        btn.disabled = false;
        btn.textContent = '✅ 我已支付完成';
        upgradeMsg.textContent = '开通失败：' + err.message;
        upgradeMsg.className = 'form-msg err';
      });
  }

  payDoneBtn.addEventListener('click', finishPay);

  // 创建体验空间
  spaceCreateBtn.addEventListener('click', function () {
    var token = getToken();
    if (!token) { showForms(); return; }
    var childName = (spaceChildName.value || '').trim() || '体验小朋友';
    spaceCreateBtn.disabled = true;
    spaceCreateBtn.textContent = '正在创建…';
    showMsg('正在创建孩子的专属空间…', true);
    post(TRIAL_API + '/spaces', { child_name: childName }, token)
      .then(function (r) {
        localStorage.setItem('easyfix_trial_key', r.key);
        // 创建即签发空间主账号 token：跳转空间后不会被登录墙拦截
        if (r.space_token) localStorage.setItem('easyfix_token', r.space_token);
        localStorage.removeItem('easyfix_kid');
        showMsg('体验空间已创建，正在进入…', true);
        window.location.href = r.url;
      })
      .catch(function (err) {
        spaceCreateBtn.disabled = false;
        spaceCreateBtn.textContent = '创建体验空间 →';
        showMsg('创建失败：' + err.message, false);
      });
  });

  // 退出登录
  spaceLogout.addEventListener('click', function () {
    localStorage.removeItem('easyfix_token');
    localStorage.removeItem('easyfix_account_token');
    localStorage.removeItem('easyfix_user');
    localStorage.removeItem('easyfix_trial_key');
    localStorage.removeItem('easyfix_kid');
    showForms();
  });

  // ---------- 提交 ----------
  function handleAccountResult(r, okMsg) {
    if (!r || !r.token) throw new Error('未获取到登录凭证');
    // 双 token：easyfix_account_token 管官网面板（升级/订阅），easyfix_token 管空间内 API
    localStorage.setItem('easyfix_account_token', r.token);
    if (r.user) localStorage.setItem('easyfix_user', JSON.stringify(r.user));
    var space = r.space;
    if (r.space_token) {
      localStorage.setItem('easyfix_token', r.space_token);
    }
    if (space && space.key) {
      localStorage.setItem('easyfix_trial_key', space.key);
      // 官网登录即进家长自己的空间（小孩选择界面），无需再次登录空间
      window.location.href = space.url;
      return;
    }
    // 老账号无空间：退回「我的空间」面板手动创建
    localStorage.removeItem('easyfix_trial_key');
    showPanel((r.user && r.user.username) || '朋友');
    presetChildName(r.user);
    renderSpace(space);
    refreshStatus(r.user, space);
    showMsg(okMsg, true);
  }

  registerForm.addEventListener('submit', function (e) {
    e.preventDefault();
    var fd = new FormData(registerForm);
    var username = (fd.get('username') || '').trim();
    var password = fd.get('password') || '';
    var ruleErr = validateRegister(username, password);
    if (ruleErr) {
      showMsg('注册失败：' + ruleErr, false);
      return;
    }
    showMsg('正在注册…', true);
    var payload = {
      username: username,
      password: password,
      role: (regRole && regRole.value) || 'parent',
    };
    post(API + '/register', payload)
      .then(function (r) {
        // 注册成功 → 新空间标记：进入空间后走「初始化引导」（小孩/家长/知识点/单词）
        sessionStorage.setItem('easyfix_new_space', '1');
        handleAccountResult(r, '注册成功');
      })
      .catch(function (err) { showMsg('注册失败：' + err.message, false); });
  });

  loginForm.addEventListener('submit', function (e) {
    e.preventDefault();
    var fd = new FormData(loginForm);
    showMsg('正在登录…', true);
    post(API + '/login', {
      username: fd.get('username'),
      password: fd.get('password'),
    })
      .then(function (r) { handleAccountResult(r, '登录成功'); })
      .catch(function (err) { showMsg('登录失败：' + err.message, false); });
  });

  // ---------- 初始化：加载配置 + 已登录（account token）直接进面板 ----------
  loadPublicConfig();
  var savedToken = localStorage.getItem('easyfix_account_token');
  if (savedToken) {
    enterPanelFromAccount(savedToken);
  }
})();
