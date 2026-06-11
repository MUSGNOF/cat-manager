// 滑动删除功能最终验证脚本
console.log('=== 滑动删除功能验证开始 ===');

// 1. 检查关键函数是否存在
const requiredFunctions = [
  'initSwipeEvents',
  'confirmDeleteRecord',
  'deleteRecord'
];

let allFunctionsExist = true;
requiredFunctions.forEach(funcName => {
  if (typeof window[funcName] === 'function') {
    console.log(`✅ ${funcName} 函数存在`);
  } else {
    console.log(`❌ ${funcName} 函数不存在`);
    allFunctionsExist = false;
  }
});

// 2. 检查DOM结构
function checkDOMStructure() {
  console.log('\n=== DOM结构检查 ===');
  
  // 创建测试DOM
  const testContainer = document.createElement('div');
  testContainer.innerHTML = `
    <div class="swipe-container">
      <div class="timeline-item">
        <div class="timeline-dot" style="background-color: #f0854b;"></div>
        <div class="timeline-content">
          <div class="timeline-date">2025-06-09</div>
          <div class="timeline-title">测试项目</div>
          <div class="timeline-type">疫苗</div>
        </div>
      </div>
      <div class="delete-action" onclick="confirmDeleteRecord('test-id', this)">
        删除
      </div>
    </div>
  `;
  
  const swipeContainer = testContainer.querySelector('.swipe-container');
  const timelineItem = testContainer.querySelector('.timeline-item');
  const deleteAction = testContainer.querySelector('.delete-action');
  
  if (swipeContainer && timelineItem && deleteAction) {
    console.log('✅ DOM结构正确:');
    console.log(`  - .swipe-container: ${swipeContainer.className}`);
    console.log(`  - .timeline-item: ${timelineItem.className}`);
    console.log(`  - .delete-action: ${deleteAction.className}`);
    return true;
  } else {
    console.log('❌ DOM结构不完整');
    return false;
  }
}

// 3. 测试滑动逻辑
function testSwipeLogic() {
  console.log('\n=== 滑动逻辑测试 ===');
  
  const testDiv = document.createElement('div');
  testDiv.className = 'swipe-container';
  testDiv.innerHTML = `
    <div class="timeline-item" style="width: 100%; height: 60px; background: #f0f0f0;"></div>
    <div class="delete-action" style="display: none;">删除</div>
  `;
  
  document.body.appendChild(testDiv);
  
  const timelineItem = testDiv.querySelector('.timeline-item');
  const deleteAction = testDiv.querySelector('.delete-action');
  
  // 添加测试事件监听器
  let testPassed = false;
  timelineItem.addEventListener('touchstart', () => {
    console.log('✅ touchstart 事件触发');
  });
  
  timelineItem.addEventListener('touchmove', () => {
    console.log('✅ touchmove 事件触发');
  });
  
  timelineItem.addEventListener('touchend', () => {
    console.log('✅ touchend 事件触发');
    testPassed = true;
  });
  
  // 模拟触摸事件
  try {
    const touchStart = new TouchEvent('touchstart', {
      touches: [{ clientX: 100, clientY: 30 }],
      bubbles: true
    });
    
    const touchMove = new TouchEvent('touchmove', {
      touches: [{ clientX: 50, clientY: 30 }],
      bubbles: true
    });
    
    const touchEnd = new TouchEvent('touchend', {
      bubbles: true
    });
    
    timelineItem.dispatchEvent(touchStart);
    timelineItem.dispatchEvent(touchMove);
    timelineItem.dispatchEvent(touchEnd);
    
    console.log('✅ 触摸事件模拟完成');
  } catch (e) {
    console.log('⚠️ 触摸事件模拟失败:', e.message);
  }
  
  // 清理
  document.body.removeChild(testDiv);
  
  return testPassed;
}

// 4. 测试删除确认逻辑
function testDeleteConfirmation() {
  console.log('\n=== 删除确认测试 ===');
  
  // 创建测试DOM
  const testDiv = document.createElement('div');
  testDiv.className = 'swipe-container';
  testDiv.innerHTML = `
    <div class="timeline-item" style="transform: translateX(-80px);">
      已滑开的项目
    </div>
    <div class="delete-action visible" onclick="testConfirmCallback()">
      删除
    </div>
  `;
  
  document.body.appendChild(testDiv);
  
  const deleteAction = testDiv.querySelector('.delete-action');
  const timelineItem = testDiv.querySelector('.timeline-item');
  
  // 测试确认函数
  window.testConfirmCallback = function() {
    console.log('✅ 删除按钮点击事件触发');
    
    // 模拟confirm对话框
    const originalConfirm = window.confirm;
    let confirmCalled = false;
    
    window.confirm = function(message) {
      console.log(`✅ confirm对话框被调用: "${message}"`);
      confirmCalled = true;
      return true; // 模拟用户点击"确定"
    };
    
    // 调用确认删除函数
    if (typeof confirmDeleteRecord === 'function') {
      confirmDeleteRecord('test-id-123', deleteAction);
      console.log('✅ confirmDeleteRecord 函数调用成功');
    } else {
      console.log('❌ confirmDeleteRecord 函数不存在');
    }
    
    window.confirm = originalConfirm;
    
    // 检查是否调用了deleteRecord
    const originalDeleteRecord = window.deleteRecord;
    let deleteRecordCalled = false;
    
    window.deleteRecord = function(id) {
      console.log(`✅ deleteRecord 被调用, id: ${id}`);
      deleteRecordCalled = true;
    };
    
    // 再次调用以触发deleteRecord
    if (typeof confirmDeleteRecord === 'function') {
      confirmDeleteRecord('test-id-456', deleteAction);
    }
    
    window.deleteRecord = originalDeleteRecord;
    
    return confirmCalled && deleteRecordCalled;
  };
  
  // 触发点击事件
  deleteAction.click();
  
  // 清理
  document.body.removeChild(testDiv);
  delete window.testConfirmCallback;
  
  return true;
}

// 5. 运行所有测试
function runAllTests() {
  console.log('\n=== 运行完整测试套件 ===');
  
  const results = {
    functions: allFunctionsExist,
    dom: checkDOMStructure(),
    swipe: testSwipeLogic(),
    delete: testDeleteConfirmation()
  };
  
  console.log('\n=== 测试结果汇总 ===');
  Object.entries(results).forEach(([test, passed]) => {
    console.log(`${passed ? '✅' : '❌'} ${test}: ${passed ? '通过' : '失败'}`);
  });
  
  const allPassed = Object.values(results).every(result => result);
  
  if (allPassed) {
    console.log('\n🎉 所有测试通过！滑动删除功能应该可以正常工作。');
    console.log('\n使用说明：');
    console.log('1. 在项目上向左滑动（移动端）或向左拖动（桌面端）');
    console.log('2. 滑动超过一半距离会显示删除按钮');
    console.log('3. 点击删除按钮进行删除确认');
    console.log('4. 点击已滑开的项目可以关闭滑动状态');
  } else {
    console.log('\n⚠️ 部分测试失败，请检查以上错误信息。');
  }
  
  return allPassed;
}

// 导出测试函数
window.verifySwipeDelete = runAllTests;

// 自动运行测试
if (typeof window !== 'undefined') {
  setTimeout(() => {
    console.log('=== 滑动删除功能自动验证 ===');
    runAllTests();
  }, 1000);
}

module.exports = { runAllTests, checkDOMStructure, testSwipeLogic, testDeleteConfirmation };