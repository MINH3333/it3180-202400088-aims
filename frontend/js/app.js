"use strict";

const API_URL = "/api/tasks";

const taskForm = document.querySelector("#task-form");
const taskTitle = document.querySelector("#task-title");
const taskDescription = document.querySelector("#task-description");
const taskList = document.querySelector("#task-list");
const emptyState = document.querySelector("#empty-state");
const loadingMessage = document.querySelector("#loading-message");
const errorMessage = document.querySelector("#error-message");
const formMessage = document.querySelector("#form-message");
const totalCount = document.querySelector("#total-count");
const completedCount = document.querySelector("#completed-count");

let tasks = [];
let currentFilter = "all";

async function requestApi(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  let data = null;
  const responseText = await response.text();
  if (responseText) {
    try {
      data = JSON.parse(responseText);
    } catch (_error) {
      throw new Error("Máy chủ trả về dữ liệu không hợp lệ.");
    }
  }

  if (!response.ok) {
    throw new Error(data?.error || "Không thể thực hiện yêu cầu.");
  }
  return data;
}

function createTaskElement(task) {
  const item = document.createElement("li");
  item.className = `task-item${task.completed ? " is-completed" : ""}`;

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.className = "task-check";
  checkbox.checked = task.completed;
  checkbox.setAttribute("aria-label", `Đánh dấu ${task.title} đã hoàn thành`);
  checkbox.addEventListener("change", () => {
    updateTask(task.id, { completed: checkbox.checked });
  });

  const content = document.createElement("div");
  content.className = "task-content";

  const title = document.createElement("h3");
  title.className = "task-title";
  title.textContent = task.title;
  content.append(title);

  if (task.description) {
    const description = document.createElement("p");
    description.className = "task-description";
    description.textContent = task.description;
    content.append(description);
  }

  const deleteButton = document.createElement("button");
  deleteButton.type = "button";
  deleteButton.className = "delete-button";
  deleteButton.textContent = "Xóa";
  deleteButton.setAttribute("aria-label", `Xóa ${task.title}`);
  deleteButton.addEventListener("click", () => deleteTask(task.id));

  item.append(checkbox, content, deleteButton);
  return item;
}

function renderTasks() {
  const visibleTasks = tasks.filter((task) => {
    if (currentFilter === "pending") return !task.completed;
    if (currentFilter === "completed") return task.completed;
    return true;
  });

  taskList.replaceChildren(...visibleTasks.map(createTaskElement));
  emptyState.hidden = visibleTasks.length > 0;
  totalCount.textContent = `${tasks.length} công việc`;
  completedCount.textContent = `${tasks.filter((task) => task.completed).length} hoàn thành`;
}

async function loadTasks() {
  loadingMessage.hidden = false;
  errorMessage.textContent = "";
  try {
    tasks = await requestApi(API_URL);
    renderTasks();
  } catch (error) {
    errorMessage.textContent = error.message;
  } finally {
    loadingMessage.hidden = true;
  }
}

async function addTask(event) {
  event.preventDefault();
  formMessage.textContent = "";
  try {
    await requestApi(API_URL, {
      method: "POST",
      body: JSON.stringify({
        title: taskTitle.value,
        description: taskDescription.value,
      }),
    });
    taskForm.reset();
    formMessage.textContent = "Đã thêm công việc.";
    await loadTasks();
  } catch (error) {
    formMessage.textContent = error.message;
  }
}

async function updateTask(taskId, changes) {
  errorMessage.textContent = "";
  try {
    await requestApi(`${API_URL}/${taskId}`, {
      method: "PATCH",
      body: JSON.stringify(changes),
    });
    await loadTasks();
  } catch (error) {
    errorMessage.textContent = error.message;
    await loadTasks();
  }
}

async function deleteTask(taskId) {
  if (!window.confirm("Bạn có chắc muốn xóa công việc này không?")) return;
  errorMessage.textContent = "";
  try {
    await requestApi(`${API_URL}/${taskId}`, { method: "DELETE" });
    await loadTasks();
  } catch (error) {
    errorMessage.textContent = error.message;
  }
}

taskForm.addEventListener("submit", addTask);

document.querySelectorAll("[data-filter]").forEach((button) => {
  button.addEventListener("click", () => {
    currentFilter = button.dataset.filter;
    document.querySelectorAll("[data-filter]").forEach((filterButton) => {
      filterButton.classList.toggle("active", filterButton === button);
    });
    renderTasks();
  });
});

loadTasks();
