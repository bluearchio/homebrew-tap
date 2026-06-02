class BluearchCore < Formula
  desc "BlueArch shared local API runtime"
  homepage "https://bluearch.io"
  url "https://dist.bluearch.io/core/v0.2.3/bluearch-core_macos_arm64"
  version "v0.2.3"
  sha256 "f9ddbe456f49ee5a277b89c12af97115629ac5a2f86f1958541a760c1f833511"
  license :cannot_represent

  depends_on arch: :arm64

  def install
    bin.install "bluearch-core_macos_arm64" => "bluearch-core"
  end

  def caveats
    <<~EOS
      BlueArch Core has been installed.

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
