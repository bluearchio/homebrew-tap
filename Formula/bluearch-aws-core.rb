class BluearchAwsCore < Formula
  desc "Shared local runtime for BlueArch AWS tools"
  homepage "https://github.com/bluearchio/bluearch-aws-core"
  url "https://github.com/bluearchio/bluearch-aws-core/releases/download/v0.2.4/bluearch-core_macos_arm64"
  version "v0.2.4"
  sha256 "d0ae237cce9feef5eea2112dca45484fae99bbf9d96b9aa758b445947d5f4012"
  license :cannot_represent

  depends_on arch: :arm64

  def install
    bin.install "bluearch-core_macos_arm64" => "bluearch-core"
  end

  def caveats
    <<~EOS
      bluearch-aws-core has been installed.

      Start the shared runtime and installed web dashboards:
        bluearch-core start --daemon

      API docs:
        http://127.0.0.1:8094/docs
    EOS
  end

  test do
    system "#{bin}/bluearch-core", "--version"
  end
end
