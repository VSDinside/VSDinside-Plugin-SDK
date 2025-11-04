#pragma once

#include "StreamDockSDK/HSDAction.h"

class HSDExampleAction : public HSDAction
{
    using HSDAction::HSDAction;

    virtual void DidReceiveSettings(const nlohmann::json& payload) override;
    virtual void KeyDown(const nlohmann::json& payload) override;
    virtual void KeyUp(const nlohmann::json& payload) override;
    virtual void SendToPlugin(const nlohmann::json& payload) override;
    virtual void WillAppear(const nlohmann::json& payload) override;
    virtual void WillDisAppear(const nlohmann::json& payload) override;
};

