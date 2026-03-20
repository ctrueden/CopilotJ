/**
 * SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "";
const normalizedApiBaseUrl = apiBaseUrl.replace(/\/+$/, "");

export const baseUrl = normalizedApiBaseUrl ? `${normalizedApiBaseUrl}/api` : "/api";
